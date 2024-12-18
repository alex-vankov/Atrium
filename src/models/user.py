from sqlalchemy import Column, String
from src.models.base import Base
import uuid
from enum import Enum as PyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    Enum,
    ForeignKey,
    String,
)


class Role(PyEnum):

    """
    Enum representing user roles.
    """
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"


class User(Base):

    """
    Database model representing "users" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    firstname = Column(String(), nullable=False)
    lastname = Column(String(), nullable=False)
    username = Column(String(), unique=True, nullable=False)
    email = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    role = Column(Enum(Role, name="role_enum"), default=Role.USER)
