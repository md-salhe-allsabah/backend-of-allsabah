"""
Account Management API Router.

This module defines the FastAPI endpoints for managing user accounts, including
user registration, retrieval, partial updates, and deletion.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Path

from Accounts_manager.models import UserCreate, UserUpdate
from db.crud import (
    create_user,
    get_all_users,
    get_user_by_id,
    remove_user,
    update_user,
)
from db.models import User

account_router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)

# Reusable path parameter definition with Swagger UI example and validation
UserIdPath = Annotated[
    int,
    Path(
        description="The unique identifier of the user.",
        examples= 1,
        ge=1,
    ),
]


@account_router.get(
    "/",
    summary="Get Registration Page Info",
)
def register() -> dict[str, str]:
    """
    Return basic metadata for the account registration route.

    Returns:
        dict[str, str]: A dictionary indicating the current page context.
    """
    return {"page": "register"}


@account_router.get(
    "/get_all_user",
    summary="Retrieve All Users",
)
def get_all_user() -> dict[str, list[dict[str, Any]]]:
    """
    Fetch all registered user accounts from the database.

    Returns:
        dict[str, list[dict[str, Any]]]: A dictionary containing a list of
        serialized user objects under the `"users"` key.
    """
    users = get_all_users()
    # if not users:
    #     return {"users": []}
    
    return {"users": [user.to_dict() for user in users]}


@account_router.post(
    "/register",
    summary="Register a New User",
)
def create_new_user(user: UserCreate) -> Any:
    """
    Create and persist a new user account.

    Takes validated user registration details, constructs a database `User`
    instance (handling password hashing internally), and saves it to the database.

    Args:
        user (UserCreate): The validated payload containing username, plain-text
            password, admin status, and optional description.

    Returns:
        Any: The result or created user record returned by the database layer.
    """
    new_user = User.create(
        name=user.name,
        password=user.password,
        admin=user.admin,
        description=user.description,
    )
    result = create_user(new_user=new_user)
    return result


@account_router.get(
    "/user/{user_id}",
    summary="Get User by ID",
)
def get_user(user_id: UserIdPath) -> dict[str, Any]:
    """
    Retrieve a single user's profile details by their unique ID.

    Args:
        user_id (int): The unique identifier of the user to fetch.

    Returns:
        dict[str, Any]: A dictionary representation of the requested user.
    """
    user = get_user_by_id(user_id=user_id)
    return user.to_dict()


@account_router.patch(
    "/user/{user_id}",
    summary="Partially Update User",
)
def update_user_data(user_id: UserIdPath, user_update: UserUpdate) -> Any:
    """
    Partially update an existing user's attributes.

    Only fields explicitly provided in the request payload are updated,
    leaving omitted fields unchanged.

    Args:
        user_id (int): The unique identifier of the user to update.
        user_update (UserUpdate): The payload containing the fields to modify.

    Returns:
        Any: The updated user record or operation status from the database layer.
    """
    data_to_update = user_update.model_dump(exclude_unset=True)
    result = update_user(user_id=user_id, updates=data_to_update)
    return result


@account_router.delete(
    "/user/{user_id}",
    summary="Delete User",
)
def delete_user(user_id: UserIdPath) -> Any:
    """
    Delete an existing user account from the database.

    Args:
        user_id (int): The unique identifier of the user to remove.

    Returns:
        Any: The deletion confirmation or result from the database layer.
    """
    deleted = remove_user(user_id)
    return deleted