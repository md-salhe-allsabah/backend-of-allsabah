"""SQLAlchemy ORM models for the application."""

from typing import Any

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from utilities.password_manager import hash_password


class User(Base):
    """Database model representing an application user.

    Attributes:
        id: Auto-incrementing primary key identifier.
        name: Full name of the user (up to 50 characters).
        admin: Flag indicating whether the user has admin privileges.
        description: Optional biographical text or user notes.
        hashed_password: SHA-256 hashed password string.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50))
    admin: Mapped[bool] = mapped_column(default=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    @classmethod
    def create(
        cls,
        name: str,
        password: str,
        admin: bool = False,
        description: str | None = None,
    ) -> "User":
        """Factory method to safely instantiate a User with a hashed password.

        Args:
            name: Full name of the user.
            password: Plain-text password to be hashed before storage.
            admin: Whether the user has admin privileges. Defaults to False.
            description: Optional short bio or notes.

        Returns:
            An unsaved User model instance ready to be added to a session.
        """
        hashed = hash_password(password=password)
        return cls(
            name=name,
            hashed_password=hashed,
            admin=admin,
            description=description,
        )

    def to_dict(self, include_password: bool = False) -> dict[str, Any]:
        """Serialize the User instance into a JSON-compatible dictionary.

        Args:
            include_password: Whether to include the hashed_password field.
                Defaults to False for security.

        Returns:
            A dictionary representation of the User's attributes.
        """
        data: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "admin": self.admin,
            "description": self.description,
        }
        if include_password:
            data["hashed_password"] = self.hashed_password
        return data

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the User."""
        return f"<User(id={self.id}, name='{self.name}', admin={self.admin})>"
