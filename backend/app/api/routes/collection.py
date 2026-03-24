from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps.current_user import get_current_user
from app.db.deps import get_db
from app.models.brand import Brand
from app.models.collection_item import CollectionItem
from app.models.fragrance import Fragrance
from app.models.user import User
from app.schemas.collection import (
    CollectionItemCreate,
    CollectionItemDetailResponse,
    CollectionItemResponse,
)

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


@router.get("/", response_model=list[CollectionItemDetailResponse])
def get_collection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(CollectionItem, Fragrance, Brand)
        .join(Fragrance, CollectionItem.fragrance_id == Fragrance.id)
        .join(Brand, Fragrance.brand_id == Brand.id)
        .filter(CollectionItem.user_id == current_user.id)
        .order_by(CollectionItem.created_at.desc())
        .all()
    )

    return [
        CollectionItemDetailResponse(
            id=item.id,
            ownership_type=item.ownership_type,
            ml_remaining=item.ml_remaining,
            personal_rating=item.personal_rating,
            times_worn=item.times_worn,
            created_at=item.created_at,
            fragrance={
                "id": fragrance.id,
                "name": fragrance.name,
                "brand": brand.name,
            },
        )
        for item, fragrance, brand in rows
    ]
