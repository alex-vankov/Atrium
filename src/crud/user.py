from sqlalchemy.orm import Session
import logging

from typing import List
import uuid

from src.common.responses import AlreadyExists, NotFound, Unauthorized, BadRequest, ForbiddenAccess
from src.core.authentication import (get_password_hash, get_current_user, verify_password, authenticate_user, create_access_token)

from src.models.user import User, Role

from src.schemas.user import (CreateUserRequest, LoginRequest, UserResponse, UpdateEmailRequest)


logger = logging.getLogger(__name__)


def is_admin(current_user: User):
    """
    Check if the user is an admin.
    """
    return current_user.role == Role.ADMIN


def is_operator(current_user: User):
    """
    Check if the user is an operator.
    """
    return current_user.role == Role.OPERATOR


def is_user(current_user: User):
    """
    Check if the user is a user.
    """
    return current_user.role == Role.USER


def email_exists(db: Session, email: str):
    """
    Check if the email exists in the database.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: CreateUserRequest):
    """
    Create a new user.
    """
    if email_exists(db, user.email):
        return AlreadyExists(content="User")

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=get_password_hash(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return f"Welcome on board, {user.firstname} {user.lastname}!"


def get_me(db: Session, current_user: User):
    """
    Get user data.
    """

    if not current_user:
        return Unauthorized()

    return UserResponse(
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        email=current_user.email,
        role=current_user.role,
    )

