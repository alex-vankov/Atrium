from fastapi import APIRouter, Depends, Header, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.common.responses import BadRequest
from typing import Optional
import logging

from src.core.authentication import get_current_user

from src.models.user import User, Role
from src.schemas.user import (CreateUserRequest, LoginRequest,
                              UpdateEmailRequest)

from src.crud.user import create_user, get_me


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me")
def me(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_me(db, user)


@router.post("/register")
def register(user: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    return create_user(db, user)
