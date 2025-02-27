import uuid

from pydantic import BaseModel, Field, field_validator, EmailStr
from src.models.user import Role
from typing import Optional
import re
from src.models.message import MessageStatus
from src.schemas.user import UserResponse
from datetime import datetime


class MessageRequest(BaseModel):

    """
    Schema for sending a message.
    """

    receiver_id: uuid.UUID = Field(min_length=36, max_length=36, examples=["123e4567-e89b-12d3-a456-426614174000"])
    content: str = Field(min_length=1, max_length=1000, examples=["Hello!"])

class MessageResponse(BaseModel):

    """
    Schema for a message response.
    """

    id: uuid.UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    created: str = Field()
    sender: UserResponse = Field()
    receiver: UserResponse = Field()
    content: str = Field()
    status: MessageStatus
    seen: datetime