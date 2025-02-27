
from src.models.message import MessageStatus, Message

from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import logging
from datetime import datetime

from typing import List, Type
import uuid

from src.common.responses import AlreadyExists, NotFound, Unauthorized, BadRequest, ForbiddenAccess
from src.core.authentication import (get_password_hash, get_current_user, verify_password, authenticate_user, create_access_token)

from src.models.user import User, Role, State, ProfileType
from src.models.search import SearchType

from src.schemas.user import (CreateUserRequest, LoginRequest, UserResponse, UpdateEmailRequest)
from src.schemas.message import MessageRequest, MessageResponse
from src.crud.friends import if_friends
from src.crud.user import get_user_by_id, is_admin, is_moderator, is_public

logger = logging.getLogger(__name__)


def format_message_response(db: Session, message: Message | Type[Message]):
    return MessageResponse(id=message.id,
                           created=message.created.strftime("%H:%M:%S %d-%m-%Y"),
                           sender=get_user_by_id(db, message.sender_id),
                           receiver=get_user_by_id(db, message.receiver_id),
                           content=message.content,
                           status=message.status,
                           seen=message.seen.strftime("%H:%M:%S %d-%m-%Y")
                           if message.seen
                           else message.seen)

def get_messages(db: Session, current_user: User):
    if not current_user:
        return Unauthorized()

    messages = db.query(Message).filter(
        or_(Message.sender_id == current_user.id, Message.receiver_id == current_user.id)
    ).all()

    return [format_message_response(db, message)
            for message in messages]

def create_message(db: Session, current_user: User, message: MessageRequest):
    if not current_user:
        return Unauthorized()

    if not if_friends(db, current_user.id, message.receiver_id) and not is_public(get_user_by_id(db, message.receiver_id)):
        return BadRequest("You are not friends with this user.")

    db_message = Message(sender_id=current_user.id,
                         receiver_id=message.receiver_id,
                         content=message.content)

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return format_message_response(db, db_message)