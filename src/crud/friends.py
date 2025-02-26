from src.schemas.friends import FriendRequest, FriendRequestResponse
from src.models.friends import Friendship, FriendshipStatus, FriendRequestAction

from pydantic import EmailStr
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
import logging
from datetime import datetime

from typing import List
import uuid

from src.common.responses import AlreadyExists, NotFound, Unauthorized, BadRequest, ForbiddenAccess
from src.core.authentication import (get_password_hash, get_current_user, verify_password, authenticate_user, create_access_token)

from src.models.user import User, Role
from src.models.search import SearchType

from src.schemas.user import (CreateUserRequest, LoginRequest, UserResponse, UpdateEmailRequest)
from src.crud.user import get_user_by_id, is_admin, is_moderator

logger = logging.getLogger(__name__)


def get_friendships_log(db: Session, current_user: User):

    if not current_user:
        return Unauthorized()

    if not is_admin(current_user) and not is_moderator(current_user):
        return ForbiddenAccess()

    friendships = db.query(Friendship).all()

    return [FriendRequestResponse(id=friendship.id,
                                  created=friendship.created.strftime("%H:%M:%S %d-%m-%Y"),
                                  sender=get_user_by_id(db, friendship.user_id),
                                  receiver=get_user_by_id(db, friendship.receiver_id),
                                  status=friendship.status,
                                  responded=friendship.responded.strftime("%H:%M:%S %d-%m-%Y")
                                  if friendship.responded
                                  else friendship.responded)
            for friendship in friendships]



def view_friends(db: Session, current_user: User):
    if not current_user:
        return Unauthorized()

    """
    View a list of friends.
    """

    friends = db.query(Friendship).filter(
        (Friendship.user_id == current_user.id) | (Friendship.receiver_id == current_user.id),
        Friendship.status == FriendshipStatus.ACCEPTED
    ).all()

    friend_ids = {
        friend.receiver_id if friend.user_id == current_user.id else friend.user_id
        for friend in friends
    }

    if not friend_ids:
        return NotFound(key="Friends", key_value="")

    return [get_user_by_id(db, friend_id) for friend_id in friend_ids]

def view_friend_requests(db: Session, current_user: User):

    if not current_user:
        return Unauthorized()


    """
    View a list of friend requests.
    """

    friend_requests = db.query(Friendship).filter(Friendship.receiver_id == current_user.id, Friendship.status == FriendshipStatus.PENDING).all()

    if not friend_requests:
        return NotFound(key="Friend requests", key_value="")

    return [FriendRequestResponse(id=friend_request.id,
                                  created=friend_request.created.strftime("%H:%M:%S %d-%m-%Y"),
                                  sender=get_user_by_id(db, friend_request.user_id),
                                  receiver=get_user_by_id(db, friend_request.receiver_id),
                                  status=friend_request.status,
                                  responded=friend_request.responded.strftime("%H:%M:%S %d-%m-%Y")
                                  if friend_request.responded
                                  else friend_request.responded)
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
    friend_request.responded = datetime.now()
    db.commit()
    db.refresh(friend_request)

    return FriendRequestResponse(id=friend_request.id,
                                 created=friend_request.created.strftime("%H:%M:%S %d-%m-%Y"),
                                 sender=get_user_by_id(db, friend_request.user_id),
                                 receiver=get_user_by_id(db, friend_request.receiver_id),
                                 status=friend_request.status,
                                 responded=friend_request.responded.strftime("%H:%M:%S %d-%m-%Y")
                                 if friend_request.responded
                                 else friend_request.responded)


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
    friend_request.responded = datetime.now()
    db.commit()
    db.refresh(friend_request)

    return FriendRequestResponse(id=friend_request.id,
                                 created=friend_request.created.strftime("%H:%M:%S %d-%m-%Y"),
                                 sender=get_user_by_id(db, friend_request.user_id),
                                 receiver=get_user_by_id(db, friend_request.receiver_id),
                                 status=friend_request.status,
                                 responded=friend_request.responded.strftime("%H:%M:%S %d-%m-%Y")
                                 if friend_request.responded
                                 else friend_request.responded)


def open_friend_request(db: Session, current_user: User, friend_request_id: uuid.UUID, action: FriendRequestAction):

    if not current_user:
        return Unauthorized()

    """
    Open a friend request.
    """

    friend_request = (db.query(Friendship).filter(Friendship.id == friend_request_id,
                                                 or_(Friendship.status == FriendshipStatus.PENDING,
                                                     Friendship.status == FriendshipStatus.SEEN))
                      .first())

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
            friend_request.status = FriendshipStatus.SEEN
            friend_request.responded = datetime.now()
            db.commit()
            db.refresh(friend_request)
            return FriendRequestResponse(id=friend_request.id,
                                         created=friend_request.created.strftime("%H:%M:%S %d-%m-%Y"),
                                         sender=get_user_by_id(db, friend_request.user_id),
                                         receiver=get_user_by_id(db, friend_request.receiver_id),
                                         status=friend_request.status,
                                         responded=friend_request.responded.strftime("%H:%M:%S %d-%m-%Y")
                                         if friend_request.responded
                                         else friend_request.responded)


def create_friend_request(db: Session, current_user: User, receiver_id: uuid.UUID):

    if not current_user:
        return Unauthorized()

    if current_user.id == receiver_id:
        return BadRequest("You cannot send a friend request to yourself.")

    receiver = db.query(User).filter(User.id == receiver_id).first()
    if not receiver:
        return NotFound("User not found.")

    """
    Create a friend request.
    """

    existing_friend_request = db.query(Friendship).filter(
        or_(
            and_(Friendship.user_id == current_user.id, Friendship.receiver_id == receiver_id),
            and_(Friendship.user_id == receiver_id, Friendship.receiver_id == current_user.id)
        )
    ).first()

    if existing_friend_request:
        if existing_friend_request.status == FriendshipStatus.PENDING:
            return AlreadyExists("Friend request already sent.")
        elif existing_friend_request.status == FriendshipStatus.ACCEPTED:
            return BadRequest("You are already friends.")
        elif existing_friend_request.status == FriendshipStatus.REJECTED:
            return BadRequest("Friend request has been rejected.")
        else:
            return BadRequest("Invalid request status.")

    new_friend_request = Friendship(
        user_id=current_user.id,
        receiver_id=receiver_id
    )
    db.add(new_friend_request)
    db.commit()
    db.refresh(new_friend_request)

    return FriendRequestResponse(
        id=new_friend_request.id,
        created=new_friend_request.created.strftime("%H:%M:%S %d-%m-%Y"),
        sender=get_user_by_id(db, new_friend_request.user_id),
        receiver=get_user_by_id(db, new_friend_request.receiver_id),
        status=new_friend_request.status,
        responded=new_friend_request.responded.strftime("%H:%M:%S %d-%m-%Y")
        if new_friend_request.responded
        else new_friend_request.responded
    )


def if_friends(db: Session, first_user: uuid.UUID, second_user: uuid.UUID):

    """
    Check if two users are friends.
    """

    friendship = db.query(Friendship).filter(
        or_(
            and_(Friendship.user_id == first_user, Friendship.receiver_id == second_user),
            and_(Friendship.user_id == second_user, Friendship.receiver_id == first_user)
        ),
        Friendship.status == FriendshipStatus.ACCEPTED
    ).first()

    if not friendship:
        return False

    return True