from src.core.authentication import get_current_user
from src.models.friends import Friendship, FriendshipStatus, FriendRequestAction
from src.schemas.friends import FriendRequestResponse
from src.models.user import User, Role
from src.crud.friends import (create_friend_request, view_friend_requests,
                              view_friends, open_friend_request, get_friendships_log)
from fastapi import APIRouter, Depends, Header, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.common.responses import BadRequest
from typing import Optional
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/log")
def get_friendships(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a log of friendships.
    """
    return get_friendships_log(db, current_user)

@router.get("/")
def get_friends(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a list of friends.
    """
    return view_friends(db, current_user)


@router.get("/requests")
def get_friend_requests(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get a list of friend requests.
    """
    return view_friend_requests(db, current_user)


@router.post("/requests")
def send_friend_request(receiver_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Send a friend request.
    """
    return create_friend_request(db, current_user, receiver_id)


@router.put("/requests/{friend_request_id}")
def respond_friend_request(friend_request_id: uuid.UUID,
                          action: Optional[FriendRequestAction] = Query(None, title="Action",
                                                                        description="Action to take on the friend request"),
                          current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Respond to a friend request.
    """
    return open_friend_request(db, current_user, friend_request_id, action)
