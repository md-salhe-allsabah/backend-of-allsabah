"""Main entry point to initialize the database and run user CRUD operations."""

import crud

from db.database import Base, engine
from db.models import User

# Ensure all tables defined on Base exist in users.db
Base.metadata.create_all(bind=engine)


def main() -> None:
    """Demonstrate all five user CRUD operations."""
    # 1. Create a user
    user_obj = User.create(
        name="Rahul",
        password="my_secret_password",
        admin=True,
        description="Lead developer",
    )
    created = crud.create_user(user_obj)
    print("Created:", created)

    user_id = int(created["id"])

    # 2. Get single user by ID
    user = crud.get_user_by_id(user_id)
    print("Single User:", user)

    # 3. Update user
    updated = crud.update_user(user_id, {"description": "Senior Python Developer"})
    print("Updated:", updated)

    # 4. Get all users
    all_users = crud.get_all_users()
    print("All Users:", all_users)

    # 5. Remove user
    deleted = crud.remove_user(user_id)
    print("Deleted:", deleted)
    users = crud.get_all_users()
    print(users.name)



if __name__ == "__main__":
    main()
