from sqlalchemy import Column, String, UniqueConstraint
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
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Friendship(Base):

    """
    Database model representing "friendships" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    __tablename__ = "friendships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(Enum(FriendshipStatus, name="friendship_status_enum"), default=FriendshipStatus.PENDING)
    __table_args__ = (
        UniqueConstraint("user_id", "receiver_id", name="unique_friendship"),
    )