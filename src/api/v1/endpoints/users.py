import uuid

from fastapi import APIRouter, Depends, Header, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.common.responses import BadRequest
from typing import Optional
import logging

from src.core.authentication import get_current_user

from src.models.user import User, Role, StateAction, ProfileType
from src.models.search import SearchType
from src.schemas.user import (CreateUserRequest, LoginRequest,
                              UpdateEmailRequest)

from src.crud.user import create_user, get_me, search_user, change_state, change_type


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return get_me(user)

@router.get("/")
def get_users(search_type: Optional[SearchType] = Query(None, title="Search type", description="Type of search"),
              search_query: Optional[str] = Query(None, title="Search query", description="Query to search for"),
              current_user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """
    Get a list of users.
    """
    return search_user(db, current_user, search_type , search_query)


@router.put("/type")
def change_user_type(current_user: User = Depends(get_current_user),
                     action: ProfileType = Query(..., title="Action", description="Action to perform"),
                     db: Session = Depends(get_db)):
    """
    Change your profile type.
    """
    return change_type(db, current_user, action)


@router.put("/state")
def change_user_state(current_user: User = Depends(get_current_user),
                      user_id: uuid.UUID = Query(..., title="User ID", description="ID of the user to change state"),
                      action: StateAction = Query(..., title="Action", description="Action to perform"),
                      db: Session = Depends(get_db)):
    """
    Change the state of a user.
    """
    return change_state(db, current_user, user_id, action)

@router.post("/")
def register(current_user: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return create_user(db, current_user)
