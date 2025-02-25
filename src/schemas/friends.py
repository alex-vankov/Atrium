import uuid

from pydantic import BaseModel, Field, field_validator, EmailStr
from src.models.user import Role
from typing import Optional
import re
from src.models.friends import FriendshipStatus


class FriendRequest(BaseModel):

    """
    Schema for sending a friend request.
    """

    receiver_id: str = Field(min_length=36, max_length=36, examples=["123e4567-e89b-12d3-a456-426614174000"])

class FriendRequestResponse(BaseModel):

    """
    Schema for a friend request response.
    """

    id: uuid.UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    user_id: uuid.UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    receiver_id: uuid.UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    status: FriendshipStatus = Field()