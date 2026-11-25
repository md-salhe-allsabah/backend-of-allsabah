import bcrypt

# Pre-computed dummy hash for timing-attack protection when a user isn't found
DUMMY_HASH = b"$2b$12$C6UzMDM.H6dfI/f/IKxGhu6X6m38gB5.Z2P2z7x0kX8fX2X2X2X2."


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        raise ValueError("Password cannot exceed 72 bytes.")

    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password_bytes, salt).decode("utf-8")


def check_password(hashed_password: str, plain_password: str) -> bool:
    password_bytes = plain_password.encode("utf-8")

    # Truncate or reject >72 bytes to prevent ValueError during login
    if len(password_bytes) > 72:
        return False

    if not hashed_password:
        bcrypt.checkpw(password_bytes, DUMMY_HASH)
        return False

    return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))


def update_password(current_hashed_password: str, old_password: str, new_password: str) -> str:
    if not check_password(current_hashed_password, old_password):
        raise ValueError("Current password is incorrect.")

    if check_password(current_hashed_password, new_password):
        raise ValueError("New password must be different from the current password.")

    return hash_password(new_password)
