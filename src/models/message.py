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


class MessageStatus(PyEnum):

    """
    Enum representing message statuses.
    """
    DELIVERED = "delivered"
    SEEN = "seen"


class Message(Base):

    """
    Database model representing "messages" table in the database.
    UUID and table name are inherited from Base.
    """

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created = Column(DateTime, default=datetime.now(), nullable=False)
    sender_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    receiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    status = Column(Enum(MessageStatus, name="message_status_enum"), default=MessageStatus.DELIVERED)
    seen = Column(DateTime, default=None, nullable=True)

    __table_args__ = (
        UniqueConstraint("sender_id", "receiver_id", "content", name="unique_message"),
    )