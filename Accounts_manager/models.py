from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for creating a new user account."""

    name: str = Field(
        ...,
        description="The username or display name of the user.",
        examples=["Allsabah"],
    )
    password: str = Field(
        ...,
        description="The plain-text password to be hashed upon creation.",
        examples=["StrongP@ss123"],
    )
    admin: bool = Field(
        default=False,
        description="Flag indicating if the user has administrative privileges.",
        examples=[False],
    )
    description: str | None = Field(
        default=None,
        description="An optional short biography or profile description.",
        examples=["I'm the first user"],
    )


class UserUpdate(BaseModel):
    """Schema for partially updating an existing user.

    All fields are optional so the client can update one or many attributes
    in a single request without overwriting omitted fields.
    """

    name: str | None = Field(
        default=None,
        description="Updated username or display name.",
        examples=["Allsabah_updated"],
    )
    admin: bool | None = Field(
        default=None,
        description="Updated administrative privilege status.",
        examples=[True],
    )
    description: str | None = Field(
        default=None,
        description="Updated biography or profile description.",
        examples=["Updated profile bio"],
    )
