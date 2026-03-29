from typing import Optional

from pydantic import BaseModel


class FragranceListItemResponse(BaseModel):
    id: int
    name: str
    brand: str
    release_year: Optional[int]
    gender_category: Optional[str]

    model_config = {"from_attributes": True}


class FragranceDetailResponse(BaseModel):
    id: int
    name: str
    brand: str
    release_year: Optional[int]
    gender_category: Optional[str]
    description: Optional[str]

    model_config = {"from_attributes": True}
