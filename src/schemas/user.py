from pydantic import BaseModel, Field, field_validator, EmailStr
from src.models.user import Role
from typing import Optional
import re


class CreateUserRequest(BaseModel):

    """
    Schema for creating a new user.
    """

    firstname: str = Field(min_length=3, max_length=50, examples=["John"])
    lastname: str = Field(min_length=3, max_length=50, examples=["Doe"])
    email: EmailStr = Field(min_length=6, max_length=50, examples=["johndoe@gmail.com"])
    password: str = Field(min_length=8, max_length=50, examples=["password"])

    @field_validator("firstname")
    def validate_firstname(cls, value):

        """
        Validate firstname to contain only alphabetic characters.
        """

        if not re.match(r"^[a-zA-Z]*$", value):
            raise ValueError("Firstname must contain only alphabetic characters")
        return value

    @field_validator("lastname")
    def validate_lastname(cls, value):

        """
        Validate lastname to contain only alphabetic characters.
        """

        if not re.match(r"^[a-zA-Z]*$", value):
            raise ValueError("Lastname must contain only alphabetic characters")
        return value

    @field_validator("password")
    def validate_password(cls, value):

        """
        Validate password to contain at least one letter and one number.
        """

        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&\-_])[A-Za-z\d@$!%*?&\-_]{8,}$", value):
            raise ValueError("Password must be at least 8 characters long"
                             " and contain at least one letter and one number and one special character")
        return value


class UpdateEmailRequest(BaseModel):

    """
    Schema for updating user data.
    """

    email: Optional[EmailStr] = Field(min_length=6, max_length=50, examples=["johndoe@gmail.com"])


class LoginRequest(BaseModel):

    """
    Schema for logging in a user.
    """

    email: EmailStr = Field(min_length=6, max_length=50, examples=["johndoe@gmail.com"])
    password: str = Field(min_length=8, max_length=50, examples=["password"])

    @field_validator("password")
    def validate_password(cls, value):

        """
        Validate password to contain at least one letter and one number.
        """

        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&\-_])[A-Za-z\d@$!%*?&\-_]{8,}$", value):
            raise ValueError("Password must be at least 8 characters long"
                             " and contain at least one letter and one number and one special character")
        return value


class UserResponse(BaseModel):

    """
    Schema for returning user data.
    """

    firstname: str
    lastname: str
    email: EmailStr
    role: Role
