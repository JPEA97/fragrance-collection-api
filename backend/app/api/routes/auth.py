import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.db.deps import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username.lower()).first()

    if not user:
        logger.warning(
            "Login failed for email=%s reason=user_not_found",
            form_data.username.lower(),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(form_data.password, user.password_hash):
        logger.warning(
            "Login failed for email=%s reason=invalid_password",
            form_data.username.lower(),
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    logger.info("Login succeeded for user_id=%s", user.id)

    access_token = create_access_token(subject=str(user.id))

    return TokenResponse(access_token=access_token)
