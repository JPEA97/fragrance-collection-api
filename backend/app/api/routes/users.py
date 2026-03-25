from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps.current_user import get_current_user
from app.core.security import hash_password
from app.db.deps import get_db
from app.models.user import User
from app.schemas.common import ItemEnvelope
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=ItemEnvelope, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter((User.email == payload.email) | (User.username == payload.username))
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )

    user = User(
        email=payload.email.lower(),
        username=payload.username,
        password_hash=hash_password(payload.password),
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return ItemEnvelope(data=UserResponse.model_validate(user))


@router.get("/me", response_model=ItemEnvelope)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return ItemEnvelope(data=UserResponse.model_validate(current_user))


@router.get("/{user_id}", response_model=ItemEnvelope)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return ItemEnvelope(data=UserResponse.model_validate(user))
