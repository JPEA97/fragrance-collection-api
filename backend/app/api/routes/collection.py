from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps.current_user import get_current_user
from app.db.deps import get_db
from app.models.collection_item import CollectionItem
from app.models.user import User
from app.schemas.collection import CollectionItemCreate, CollectionItemResponse

router = APIRouter(prefix="/collection", tags=["collection"])


@router.post(
    "/", response_model=CollectionItemResponse, status_code=status.HTTP_201_CREATED
)
def add_to_collection(
    payload: CollectionItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = CollectionItem(
        user_id=current_user.id,
        fragrance_id=payload.fragrance_id,
        ownership_type=payload.ownership_type,
        ml_remaining=payload.ml_remaining,
        personal_rating=payload.personal_rating,
    )

    db.add(item)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already exists or fragrance is invalid",
        )

    db.refresh(item)
    return item
