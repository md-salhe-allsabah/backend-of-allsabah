"""Pydantic schemas for validating user authentication requests and responses."""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Schema for incoming user login credentials.

    Attributes:
        user_id: The unique positive integer primary key ID of the user.
        password: The plain-text password submitted by the user (1-72 bytes).
    """

    user_id: int = Field(
        ...,
        gt=0,
        description="Unique integer ID of the user.",
        examples=[1],
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=72,
        description="Plain-text user password (maximum 72 bytes for bcrypt).",
        examples=["MySecret123"],
    )


class LoginResponse(BaseModel):
    """Schema for successful user authentication responses.

    Attributes:
        authenticated: Boolean flag confirming the credentials were verified.
        user_id: The unique integer ID of the authenticated user.
        message: Human-readable status message.
    """

    authenticated: bool
    user_id: int
    message: str
