from src.schemas.friends import FriendRequest, FriendRequestResponse
from src.models.friends import Friendship, FriendshipStatus, FriendRequestAction

from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import logging

from typing import List
import uuid

from src.common.responses import AlreadyExists, NotFound, Unauthorized, BadRequest, ForbiddenAccess
from src.core.authentication import (get_password_hash, get_current_user, verify_password, authenticate_user, create_access_token)

from src.models.user import User, Role
from src.models.search import SearchType

from src.schemas.user import (CreateUserRequest, LoginRequest, UserResponse, UpdateEmailRequest)
from src.crud.user import get_user_by_id


logger = logging.getLogger(__name__)


def view_friends(db: Session, current_user: User):

    if not current_user:
        return Unauthorized()

    """
    View a list of friends.
    """

    friends = (db.query(Friendship).filter(Friendship.user_id == current_user.id, Friendship.status == FriendshipStatus.ACCEPTED).all())
    friends1 = (db.query(Friendship).filter(Friendship.receiver_id == current_user.id, Friendship.status == FriendshipStatus.ACCEPTED).all())

    if friends:
        return [get_user_by_id(db, friend.receiver_id) for friend in friends]

    if friends1:
        return [get_user_by_id(db, friend.user_id) for friend in friends1]



    return NotFound(key="Friends", key_value="")


def view_friend_requests(db: Session, current_user: User):

    if not current_user:
        return Unauthorized()


    """
    View a list of friend requests.
    """

    friend_requests = db.query(Friendship).filter(Friendship.receiver_id == current_user.id, Friendship.status == FriendshipStatus.PENDING).all()

    if not friend_requests:
        return NotFound(key="Friend requests", key_value="")

    return [FriendRequestResponse(id=friend_request.id, user_id=friend_request.user_id,
                                  receiver_id=friend_request.receiver_id, status=friend_request.status)
            for friend_request in friend_requests]

def accept_friend_request(db: Session, current_user: User, friend_request: Friendship):

    if not current_user:
        return Unauthorized()

    """
    Accept a friend request.
    """

    if friend_request.receiver_id != current_user.id:
        return ForbiddenAccess()

    if not friend_request:
        return NotFound(key="Friend request", key_value="")

    friend_request.status = FriendshipStatus.ACCEPTED
    db.commit()

    return FriendRequestResponse(id=friend_request.id, user_id=friend_request.user_id,
                                 receiver_id=friend_request.receiver_id, status=friend_request.status)


def reject_friend_request(db: Session, current_user: User, friend_request: Friendship):

    if not current_user:
        return Unauthorized()

    """
    Reject a friend request.
    """

    if friend_request.receiver_id != current_user.id:
        return ForbiddenAccess()

    if not friend_request:
        return NotFound(key="Friend request", key_value="")

    friend_request.status = FriendshipStatus.REJECTED
    db.commit()

    return FriendRequestResponse(id=friend_request.id, user_id=friend_request.user_id,
                                 receiver_id=friend_request.receiver_id, status=friend_request.status)


def open_friend_request(db: Session, current_user: User, friend_request_id: uuid.UUID, action: FriendRequestAction):

    if not current_user:
        return Unauthorized()

    """
    Open a friend request.
    """

    friend_request = db.query(Friendship).filter(Friendship.id == friend_request_id).first()

    if not friend_request:
        return NotFound(key="Friend request", key_value="")

    if friend_request.receiver_id != current_user.id:
        return ForbiddenAccess()

    match action:
        case FriendRequestAction.ACCEPT:
            return accept_friend_request(db, current_user, friend_request)
        case FriendRequestAction.REJECT:
            return reject_friend_request(db, current_user, friend_request)
        case _:
            return friend_request


def create_friend_request(db: Session, current_user: User, receiver_id: uuid.UUID):

    if not current_user:
        return Unauthorized()

    if current_user.id == receiver_id:
        return BadRequest("You cannot send a friend request to yourself.")

    """
    Create a friend request.
    """

    existing_friend_request = db.query(Friendship).filter(or_
                                                          (and_(Friendship.user_id == current_user.id,
                                                               Friendship.receiver_id == receiver_id),
                                                          and_(Friendship.user_id == receiver_id,
                                                               Friendship.receiver_id == current_user.id
                                                               ))).first()

    if existing_friend_request:
        match existing_friend_request.status:
            case FriendshipStatus.PENDING:
                return AlreadyExists("Friend request")
            case FriendshipStatus.ACCEPTED:
                return BadRequest("You are already friends.")
            case FriendshipStatus.REJECTED:
                return BadRequest("Friend request rejected.")
            case _:
                return BadRequest("Bad request.")

    new_friend_request = Friendship(user_id=current_user.id, receiver_id=receiver_id)
    db.add(new_friend_request)
    db.commit()

    return FriendRequestResponse(id=new_friend_request.id, user_id=new_friend_request.user_id,
                                 receiver_id=new_friend_request.receiver_id, status=new_friend_request.status)


def if_friends(db: Session, current_user: User, friend_request: Friendship):

    if not current_user:
        return Unauthorized()

    """
    Check if two users are friends.
    """

    friend_request = db.query(Friendship).filter(Friendship.user_id == current_user.id,
                                                 Friendship.receiver_id == friend_request.receiver_id,
                                                 Friendship.status == FriendshipStatus.ACCEPTED).first()

    if not friend_request:
        return False

    return FriendRequestResponse(id=friend_request.id, user_id=friend_request.user_id,
                                 receiver_id=friend_request.receiver_id, status=friend_request.status)