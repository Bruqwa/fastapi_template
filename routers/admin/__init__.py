from fastapi import (
    APIRouter,
    Depends,
)
from services.fastapi_template.depends.admin_area import check_rule
from . import (
    users,
)


def register_routers(app):
    router = APIRouter(
        prefix='/api/v1/admin',
        dependencies=[Depends(check_rule)]
    )

    router.include_router(users.router)
    app.include_router(router)
    return app
