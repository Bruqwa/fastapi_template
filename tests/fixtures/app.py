import pytest
from asgi_lifespan import LifespanManager
from services.fastapi_template.main import factory
from misc import db, config
from misc.ctrl import CONFIG_ENV_KEY
from async_asgi_testclient import TestClient
import os


@pytest.fixture
async def app():
    instance = factory()
    async with LifespanManager(instance):
        yield instance


@pytest.fixture
async def client(app):
    return TestClient(app)


@pytest.fixture
async def db_pool(app):
    return app.state.db_pool


@pytest.fixture
async def conf():
    config_path = os.environ[CONFIG_ENV_KEY]
    return config.read_config(config_path)


@pytest.fixture
async def resetdb(db_pool):
    await db_pool.execute('TRUNCATE users CASCADE')
    await db_pool.execute('TRUNCATE admin_users CASCADE')
    await db_pool.execute('TRUNCATE goods CASCADE')
