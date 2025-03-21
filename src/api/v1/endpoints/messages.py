from src.core.authentication import get_current_user
from src.models.friends import Friendship, FriendshipStatus, FriendRequestAction
from src.schemas.message import MessageRequest
from src.models.user import User, Role
from src.crud.message import get_messages, create_message, open_chat
from fastapi import APIRouter, Depends, Header, Query
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.common.responses import BadRequest
from typing import Optional
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_all_messages(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a list of messages.
    """
    return get_messages(db, current_user)

@router.get("/{user_id}")
def see_chat(user_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Open a chat with a user.
    """
    return open_chat(db, current_user, user_id)

@router.post("/")
def send_message(message: MessageRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Send a message.
    """
    return create_message(db, current_user, message)