from pydantic import EmailStr
from sqlalchemy.orm import Session
import logging

from typing import List, Type
import uuid

from src.common.responses import AlreadyExists, NotFound, Unauthorized, BadRequest, ForbiddenAccess
from src.core.authentication import (get_password_hash, get_current_user, verify_password, authenticate_user, create_access_token)

from src.models.user import User, Role, State, StateAction, ProfileType
from src.models.search import SearchType

from src.schemas.user import (CreateUserRequest, LoginRequest, UserResponse, UpdateEmailRequest)


logger = logging.getLogger(__name__)


def is_admin(user: User):
    """
    Check if the user is an admin.
    """
    return user.role == Role.ADMIN


def is_moderator(user: User):
    """
    Check if the user is an operator.
    """
    return user.role == Role.MODERATOR


def is_user(user: User):
    """
    Check if the user is a user.
    """
    return user.role == Role.USER

def is_public(user: User):
    """
    Check if the user profile is public.
    """
    return user.type == ProfileType.PUBLIC


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


def format_user_response(user: User | Type[User]):
    return UserResponse(
        id=user.id,
        firstname=user.firstname,
        lastname=user.lastname,
        username=user.username,
        email=user.email,
        role=user.role,
        state=user.state,
        type=user.type
    )


def change_state(db: Session, current_user: User , user_id: uuid.UUID, action: StateAction):
    """
    Change the state of a user.
    """

    if not is_admin(current_user) and not is_moderator(current_user):
        return ForbiddenAccess()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return NotFound(key="User", key_value=f"{user_id}")

    if action == StateAction.ACTIVATE:
        user.state = State.ACTIVE
    elif action == StateAction.DEACTIVATE:
        user.state = State.INACTIVE
    elif action == StateAction.DELETE:
        user.state = State.DELETED

    db.commit()
    db.refresh(user)

    return format_user_response(user)


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

    return format_user_response(db_user)


def get_me(current_user: User):
    """
    Get user data.
    """

    if not current_user:
        return Unauthorized()

    return format_user_response(current_user)

def get_user_by_id(db: Session, user_id: uuid.UUID):
    """
    Get a user by user_id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return NotFound(key="User", key_value="")
    return format_user_response(user)

def search_user(db: Session, current_user: User, search_type: SearchType, search_value: str):
    """
    Search for users by role, username, or email. Lists all users if no search type or value is provided.
    Admins and moderators can view all users, others can only see active users.
    """
    if not current_user:
        return Unauthorized()

    if bool(search_type) ^ bool(search_value):  # XOR check for one without the other
        return BadRequest("Search type and query must be provided together.")

    # Determine if user can view all users or only active ones
    filter_active = not (is_admin(current_user) or is_moderator(current_user))

    # Base query with conditional filtering for active users
    query = db.query(User)
    if filter_active:
        query = query.filter(User.state == State.ACTIVE)

    # Apply search filters
    if search_type == SearchType.ROLE:
        query = query.filter(User.role == search_value.upper())
    elif search_type == SearchType.USERNAME:
        query = query.filter(User.username.ilike(f"%{search_value}%"))
    elif search_type == SearchType.EMAIL:
        query = query.filter(User.email.ilike(f"%{search_value}%"))

    # Execute the query
    users = query.all() if not search_type else [query.first()]

    if not users or users == [None]:
        key = "User" if search_type else "Users"
        return NotFound(key=key, key_value=search_value)

    return [format_user_response(user) for user in users] if isinstance(users, list) else format_user_response(users[0])

def change_type(db: Session, current_user: User, action: ProfileType):

    """
    Change the profile type of user.
    """

    if not current_user:
        return Unauthorized()

    user = db.query(User).filter(User.id == current_user.id).first()

    if action == ProfileType.PUBLIC:
        user.type = ProfileType.PUBLIC
    elif action == ProfileType.PRIVATE:
        user.type = ProfileType.PRIVATE

    db.commit()
    db.refresh(user)

    return format_user_response(user)