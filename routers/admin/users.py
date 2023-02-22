from fastapi import (
    APIRouter,
    Depends,
)
from misc import db
from misc.fastapi.depends.session import get as get_session
from misc.fastapi.depends.db import get as get_db
from misc.session import Session
from db import users as db_users
from models.users import (
    UsersListSuccessResponse,
    UsersListData,
    UsersSuccessResponse,
    NewUser,

)
from misc.handlers import (
    error_404,
    ErrorResponse,
)
from typing import (
    Optional,
    Union,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=['admin users']
)


@router.get('/users', response_model=UsersListSuccessResponse)
async def get_list(
        en: bool = None,
        username: str = None,
        email: str = None,
        page: int = 1,
        session: Session = Depends(get_session),
        conn: db.Connection = Depends(get_db),

) -> Optional[Union[UsersListSuccessResponse, ErrorResponse]]:
    limit = 20
    page = max(1, page)
    result = await db_users.get_users_for_admin(
        conn=conn,
        en=en,
        username=username,
        email=email,
        page=page,
        limit=limit,
    )
    total = await db_users.get_total_for_admin(
        conn=conn,
        en=en,
        username=username,
        email=email,
    )
    if not result:
        return await error_404()
    return UsersListSuccessResponse(
        data=UsersListData(
            total=total,
            page=page,
            limit=limit,
            items=result
        )
    )


@router.get('/users/{pk}', response_model=UsersSuccessResponse)
async def get_user_for_admin(
        pk: int,
        conn: db.Connection = Depends(get_db),
        session: Session = Depends(get_session),
) -> Optional[Union[UsersSuccessResponse, ErrorResponse]]:
    result = await db_users.get_user_for_admin(conn, pk)
    if not result:
        return await error_404()
    return UsersSuccessResponse(
        data=result
    )


@router.post('/users/{pk}', response_model=UsersSuccessResponse)
async def admin_update_user(
        pk: int,
        new_user: NewUser,
        conn: db.Connection = Depends(get_db),
        session: Session = Depends(get_session),
) -> Optional[Union[UsersSuccessResponse, ErrorResponse]]:
    result = await db_users.admin_update_user(conn, pk, new_user)
    if not result:
        return await error_404()
    return UsersSuccessResponse(
        data=result
    )


@router.delete('/users/{pk}', response_model=UsersSuccessResponse)
async def admin_delete_user(
        pk: int,
        conn: db.Connection = Depends(get_db),
        session: Session = Depends(get_session)
) -> Optional[Union[UsersSuccessResponse, ErrorResponse]]:
    result = await db_users.delete_user(conn, pk)
    if not result:
        return await error_404()
    return UsersSuccessResponse(
        data=result
    )
