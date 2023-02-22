import datetime
from models.base import (
    SuccessResponse,
    ListData
)
from typing import (
    List,
    Optional,
)
from pydantic import (
    BaseModel,
    Field,
)


class AdminModel(BaseModel):
    user_id: int
    en: bool
    ctime: Optional[datetime.datetime] = Field(None, nullable=True)
    atime: Optional[datetime.datetime] = Field(None, nullable=True)
    dtime: Optional[datetime.datetime] = Field(None, nullable=True)


class NewAdmin(BaseModel):
    user_id: int
    en: bool


class AdminSuccessResponse(SuccessResponse):
    data: AdminModel


class AdminListData(ListData):
    items: List[AdminModel] = []


class AdminListSuccessResponse(SuccessResponse):
    data: AdminListData
