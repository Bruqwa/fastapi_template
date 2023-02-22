from fastapi import (
    APIRouter,
    Depends,
)
from models.users import (
    UsersListSuccessResponse,
    UsersListData,
    UsersSuccessResponse,
)
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.session import get as get_session
from misc.session import Session
from misc import db
from misc.handlers import error_404
from db import users as db_users

router = APIRouter(
    tags=['users']
)


@router.get('/users', response_model=UsersListSuccessResponse)
async def get_users(
        conn: db.Connection = Depends(get_db),
        session: Session = Depends(get_session),
        page: int = 1
):
    limit = 20
    result = await db_users.get_users(
        conn=conn,
        limit=limit,
        page=page
    )
    if not result:
        return await error_404()
    total = await db_users.get_total(
        conn=conn,
    )
    return UsersListSuccessResponse(
        data=UsersListData(
            total=total,
            page=page,
            limit=limit,
            items=result
        )
    )


@router.get('/users/{pk}', response_model=UsersSuccessResponse)
async def get_user(
        pk: int,
        conn: db.Connection = Depends(get_db),
        session: Session = Depends(get_session),
):
    result = await db_users.get_user(
        conn=conn,
        pk=pk,
    )
    if not result:
        return await error_404()
    return UsersSuccessResponse(
        data=result
    )
