import logging
from typing import (
    Optional,
    List,
)
from models.goods import (
    Good,
    NewGood,

)
from misc import db

logger = logging.getLogger(__name__)

TABLE = 'goods'


async def create_good(
        conn: db.Connection,
        good: NewGood
) -> Optional[Good]:
    data = good.dict()
    result = await db.create(conn, TABLE, data)
    return db.record_to_model(Good, result)


async def update_good(
        conn: db.Connection,
        good: NewGood
) -> Optional[Good]:
    data = good.dict()
    result = await db.update(conn=conn, table=TABLE, data=data, with_atime=True)
    return db.record_to_model(Good, result)


async def get_goods(
        conn: db.Connection,
        pk: int,
) -> Optional[Good]:
    values = [pk]
    query = f'SELECT * FROM {TABLE} WHERE id = $1'
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(Good, result)


async def get_all_goods(
        limit: int,
        conn: db.Connection,
        page: int = None,

) -> Optional[List[Good]]:
    offset = limit * (page - 1)
    values = [limit, offset]
    where = f'WHERE en'
    query = f'''SELECT * FROM {TABLE} {where} 
        ORDER BY name ASC LIMIT $1 OFFSET $2'''
    result = await conn.fetch(query, *values)
    return db.record_to_model_list(Good, result)


async def get_total(
        conn: db.Connection,
) -> int:
    query = f'''SELECT count(*) FROM {TABLE}'''
    result = await conn.fetchrow(query)
    return result['count']
