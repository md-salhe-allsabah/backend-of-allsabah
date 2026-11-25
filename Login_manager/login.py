from fastapi import APIRouter, HTTPException, status

from db.crud import get_hashed_password_of_user
from Login_manager.models import LoginRequest, LoginResponse
from utilities.password_manager import check_password

login_router = APIRouter( prefix="/login",
    tags=["logins"],)

@login_router.post(
    "/pass_auth",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    responses={
        401: {"description": "Invalid user ID or password."},
        422: {"description": "Request payload validation error."},
    },
)
def login(payload: LoginRequest) -> LoginResponse:
    """Authenticate a user by verifying their ID and plain-text password.

    Fetches the stored bcrypt hash for the given `user_id` and compares it
    against the submitted password in constant time. Returns a generic 401
    error on failure to prevent user ID enumeration.

    Args:
        payload: Validated `LoginRequest` containing `user_id` and `password`.

    Returns:
        A `LoginResponse` confirming successful authentication.

    Raises:
        HTTPException: 401 Unauthorized if the user ID does not exist or the
            password does not match.
    """
    stored_hash = get_hashed_password_of_user(payload.user_id)
    is_valid = check_password(stored_hash or "", payload.password)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID or password",
        )

    return LoginResponse(
        authenticated=True,
        user_id=payload.user_id,
        message="Login successful",
    )