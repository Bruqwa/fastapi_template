from typing import (
    Optional,
)
from misc import db
from models.admin import (
    AdminModel,
)

TABLE = 'admin_users'


async def check_rules(
        conn: db.Connection,
        user_id: int,
) -> Optional[AdminModel]:
    query = f'SELECT * FROM {TABLE} WHERE user_id = $1'
    values = [user_id]
    result = await conn.fetchrow(query, *values)
    return db.record_to_model(AdminModel, result)
