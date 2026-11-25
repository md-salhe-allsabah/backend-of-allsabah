"""CRUD operations for managing User records in the SQLite database."""

import hashlib

from sqlalchemy import select

from db.database import SessionLocal
from db.models import User


def create_user(new_user: User) -> dict[str, bool | int]:
    """Persist a new User instance into the database.

    Args:
        new_user: An unsaved User instance (created via User.create()).

    Returns:
        A dictionary containing creation status ('created') and the
        auto-generated database primary key ('id').
    """
    with SessionLocal() as session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return {
            "created": True,
            "id": new_user.id,
        }


def get_all_users() -> list[User]:
    """Retrieve all user records from the database.

    Returns:
        A list of all User instances stored in the users table.
    """
    with SessionLocal() as session:
        return list(session.scalars(select(User)).all())


def get_user_by_id(user_id: int) -> User | None:
    """Retrieve a single user from the database by their ID.

    Args:
        user_id: The unique integer primary key ID of the user.

    Returns:
        The matching User instance if found, otherwise None.
    """
    with SessionLocal() as session:
        return session.get(User, user_id)


def update_user(user_id: int, updates: dict) -> dict[str, bool | int | str]:
    """Update specific attributes of an existing user record.

    Args:
        user_id: The unique integer primary key ID of the user to update.
        updates: A dictionary mapping column names ('name', 'admin',
            'description', 'password', 'hashed_password') to new values.

    Returns:
        A dictionary indicating whether the update succeeded ('updated'),
        along with the user's 'id' and 'name' (or an 'error' message).
    """
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return {"updated": False, "error": "User not found"}

        if "name" in updates:
            user.name = updates["name"]
        if "admin" in updates:
            user.admin = updates["admin"]
        if "description" in updates:
            user.description = updates["description"]
        if "password" in updates:
            user.hashed_password = hashlib.sha256(
                updates["password"].encode()
            ).hexdigest()
        elif "hashed_password" in updates:
            user.hashed_password = updates["hashed_password"]

        session.commit()
        session.refresh(user)

        return {"updated": True, "id": user.id, "name": user.name}


def remove_user(user_id: int) -> dict[str, bool | int | str]:
    """Remove a user record from the database by their ID.

    Args:
        user_id: The unique integer primary key ID of the user to delete.

    Returns:
        A dictionary confirming deletion status ('deleted') and the removed
        user's 'id' (or an 'error' message if the user was not found).
    """
    with SessionLocal() as session:
        user = session.get(User, user_id)
        if not user:
            return {"deleted": False, "error": "User not found"}

        session.delete(user)
        session.commit()

        return {"deleted": True, "id": user_id}
    
def get_hashed_password_of_user(user_id: int) -> str | None:
    """Retrieve only the stored hashed password for a given user ID."""
    with SessionLocal() as session:
        stmt = select(User.hashed_password).where(User.id == user_id)
        return session.scalar(stmt)