from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CollectionItemCreate(BaseModel):
    fragrance_id: int
    ownership_type: str = Field(pattern="^(full_bottle|decant|sample)$")
    ml_remaining: Optional[float] = None
    personal_rating: Optional[int] = Field(default=None, ge=1, le=10)

    model_config = {"extra": "forbid"}


class CollectionFragranceResponse(BaseModel):
    id: int
    name: str
    brand: str


class CollectionItemResponse(BaseModel):
    id: int
    fragrance_id: int
    ownership_type: str
    ml_remaining: Optional[float]
    personal_rating: Optional[int]
    times_worn: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CollectionItemDetailResponse(BaseModel):
    id: int
    ownership_type: str
    ml_remaining: Optional[float]
    personal_rating: Optional[int]
    times_worn: int
    created_at: datetime
    fragrance: CollectionFragranceResponse
