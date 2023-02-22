from datetime import datetime
from typing import Optional, List
from .base import (
    SuccessResponse,
    ListData,
)
from pydantic import (
    BaseModel,
    Field
)


class Good(BaseModel):
    id: int = 0
    en: Optional[bool]
    name: Optional[str] = ''
    description: Optional[str] = ''
    ctime: Optional[datetime] = Field(None, nullable=True)
    atime: Optional[datetime] = Field(None, nullable=True)
    dtime: Optional[datetime] = Field(None, nullable=True)


class NewGood(BaseModel):
    name: Optional[str]
    description: Optional[str] = ''


class GoodsSuccessResponse(SuccessResponse):
    data: Good


class GoodsListData(ListData):
    items: List[Good]


class GoodsListSuccessResponse(SuccessResponse):
    data: GoodsListData
