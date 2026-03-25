from typing import Any, Optional

from pydantic import BaseModel


class MetaResponse(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    count: Optional[int] = None


class ItemEnvelope(BaseModel):
    data: Any


class ListEnvelope(BaseModel):
    data: list[Any]
    meta: Optional[MetaResponse] = None
