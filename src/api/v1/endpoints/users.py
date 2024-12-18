from fastapi import APIRouter, Depends, Header, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.common.responses import BadRequest
from typing import Optional
import logging

from src.core.authentication import get_current_user

from src.models.user import User, Role
from src.models.search import SearchType
from src.schemas.user import (CreateUserRequest, LoginRequest,
                              UpdateEmailRequest)

from src.crud.user import create_user, get_me, search_user


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return get_me(user)

@router.get("/")
def get_users(search_type: Optional[SearchType] = Query(None, title="Search type", description="Type of search"),
              search_query: Optional[str] = Query(None, title="Search query", description="Query to search for"),
              user: User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """
    Get a list of users.
    """
    return search_user(db, user, search_type , search_query)


@router.post("/")
def register(user: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return create_user(db, user)
