from fastapi import (
    APIRouter,
    Depends,
)
from models.goods import (
    Good,
    NewGood,
    GoodsSuccessResponse,
    GoodsListData,
    GoodsListSuccessResponse
)
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.session import get as get_session
from misc.session import Session
from misc import db
from misc.handlers import error_404
from db import goods as db_goods

router = APIRouter(
    tags=['goods']
)


@router.post('/goods', response_model=GoodsSuccessResponse)
async def create_good(
        good: NewGood,
        conn: db.Connection = Depends(get_db),
):
    result = await db_goods.create_good(conn, good)
    if not result:
        return await error_404()
    return GoodsSuccessResponse(data=result)


@router.get('/goods/', response_model=GoodsSuccessResponse)
async def get_goods(
        pk: int,
        conn: db.Connection = Depends(get_db),
):
    result = await db_goods.get_goods(
        conn=conn,
        pk=pk,
    )
    if not result:
        return await error_404()
    return GoodsSuccessResponse(data=result)


@router.get('/goods/all', response_model=GoodsListSuccessResponse)
async def get_all_goods(
        conn: db.Connection = Depends(get_db),
        page: int = 1
):
    limit = 2
    result = await db_goods.get_all_goods(
        conn=conn,
        limit=limit,
        page=page
    )
    if not result:
        return await error_404()
    total = await db_goods.get_total(
        conn=conn,
    )
    return GoodsListSuccessResponse(
        data=GoodsListData(
            total=total,
            page=page,
            limit=limit,
            items=result
        )
    )
