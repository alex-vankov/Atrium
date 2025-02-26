from sqlalchemy import Column, String, UniqueConstraint, DateTime
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
from datetime import datetime


class FriendRequestAction(PyEnum):

    """
    Enum representing friend request actions.
    """
    ACCEPT = "accept"
    REJECT = "reject"


class FriendshipStatus(PyEnum):

    """
    Enum representing friendship statuses.
    """
    PENDING = "pending"
    SEEN = "seen"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Friendship(Base):

    """
    Database model representing "friendships" table in the database.
    UUID and table name are inherited from Base.
    """

    __tablename__ = "friendships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created = Column(DateTime, default=datetime.now(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(FriendshipStatus, name="friendship_status_enum"), default=FriendshipStatus.PENDING)
    responded = Column(DateTime, default=None, nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "receiver_id", name="unique_friendship"),
    )