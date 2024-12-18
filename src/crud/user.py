from pydantic import EmailStr
from sqlalchemy.orm import Session
import logging

from typing import List
import uuid

from src.common.responses import AlreadyExists, NotFound, Unauthorized, BadRequest, ForbiddenAccess
from src.core.authentication import (get_password_hash, get_current_user, verify_password, authenticate_user, create_access_token)

from src.models.user import User, Role
from src.models.search import SearchType

from src.schemas.user import (CreateUserRequest, LoginRequest, UserResponse, UpdateEmailRequest)


logger = logging.getLogger(__name__)


def is_admin(current_user: User):
    """
    Check if the user is an admin.
    """
    return current_user.role == Role.ADMIN


def is_moderator(current_user: User):
    """
    Check if the user is an operator.
    """
    return current_user.role == Role.MODERATOR


def is_user(current_user: User):
    """
    Check if the user is a user.
    """
    return current_user.role == Role.USER


def email_exists(db: Session, email: EmailStr):
    """
    Check if the email exists in the database.
    """
    return db.query(User).filter(User.email == email).first()

def username_exists(db: Session, username: str):
    """
    Check if the username exists in the database.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: CreateUserRequest):
    """
    Create a new user.
    """
    if username_exists(db, user.username):
        return AlreadyExists(content="Username")

    if email_exists(db, user.email):
        return AlreadyExists(content="User")

    db_user = User(
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=str(user.email),
        password=get_password_hash(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        firstname=db_user.firstname,
        lastname=db_user.lastname,
        username=db_user.username,
        email=db_user.email,
        role=db_user.role,
    )


def get_me(current_user: User):
    """
    Get user data.
    """

    if not current_user:
        return Unauthorized()

    return UserResponse(
        firstname=current_user.firstname,
        lastname=current_user.lastname,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
    )

def search_user(db: Session, user: User , search_type: SearchType,  search_value: str):
    """
    Search for a user by user_id.
    """
    if not user:
        return Unauthorized()

    # if not search_type and search_value:
    #     return BadRequest("Search type and query must be provided together.")
    # if not search_value and search_type:
    #     return BadRequest("Search type and query must be provided together.")
    if not search_value and not search_type:
        users = db.query(User).all()
        if not users:
            return NotFound(key="Users", key_value=search_value)
        return [UserResponse(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            role=user.role
        ) for user in users]

    if search_type == SearchType.ROLE:
        users = db.query(User).filter(User.role == search_value.upper()).all()
        if not users:
            return NotFound(key="Users", key_value=search_value)
        return [UserResponse(
            firstname=user.firstname,
            lastname=user.lastname,
            username=user.username,
            email=user.email,
            role=user.role
        ) for user in users]

    if search_type == SearchType.USERNAME:
        users = db.query(User).filter(User.username.like(f"%{search_value}%")).first()
        if not users:
            return NotFound(key="User", key_value=search_value)
        return UserResponse(firstname=users.firstname,
                            lastname=users.lastname,
                            username=users.username,
                            email=users.email,
                            role=users.role
        )

    if search_type == SearchType.EMAIL:
        users = db.query(User).filter(User.email.like(f"%{search_value}%")).first()
        if not users:
            return NotFound(key="User", key_value=search_value)
        return UserResponse(firstname=users.firstname,
                            lastname=users.lastname,
                            username=users.username,
                            email=users.email,
                            role=users.role
        )

