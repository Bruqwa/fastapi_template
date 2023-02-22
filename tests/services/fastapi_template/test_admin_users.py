import asyncio
import pytest
from tests.fixtures.auth import register_user
import logging
import datetime

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_delete_user(resetdb, client, mailhog, db_pool):
    auth_user_1, auth_user_2, auth_user_3, auth_user_4 = await users_for_test(client, mailhog, db_pool)
    get = await client.delete(f'/api/v1/admin/users/{auth_user_3["id"]}', query_string={'pk': auth_user_3["id"]})
    logger.exception(f'{auth_user_3["id"]=}')
    logger.exception(f'{get.json()=}')
    assert get.status_code == 200
    assert not get.json()['data']['en']
    assert get.json()['data']['id'] == auth_user_3['id']
    assert get.json()['data']['name'] == auth_user_3['name']


@pytest.mark.asyncio
async def test_edit_user(resetdb, client, mailhog, db_pool):
    auth_user_1, auth_user_2, auth_user_3, auth_user_4 = await users_for_test(client, mailhog, db_pool)
    data = {
        'name': 'TestNewName',
        'email': 'test@gmail.com',
    }
    get = await client.post(f'/api/v1/admin/users/{auth_user_3["id"]}', json=data)
    assert get.status_code == 200
    assert get.json()['data']['id'] == auth_user_3['id']
    assert get.json()['data']['name'] == 'TestNewName'


@pytest.mark.asyncio
async def test_get_user(resetdb, client, mailhog, db_pool):
    auth_user_1, auth_user_2, auth_user_3, auth_user_4 = await users_for_test(client, mailhog, db_pool)
    get = await client.get(f'/api/v1/admin/users/{auth_user_3["id"]}', query_string={'pk': auth_user_3['id']})
    assert get.status_code == 200
    assert get.json()['data']['id'] == auth_user_3['id']
    assert get.json()['data']['name'] == 'user_3'


@pytest.mark.asyncio
async def test_admin_search_users(resetdb, client, mailhog, db_pool):
    auth_user_1, auth_user_2, auth_user_3, auth_user_4 = await users_for_test(client, mailhog, db_pool)
    get = await client.get(f'/api/v1/admin/users')
    assert get.status_code == 200
    assert get.json()['data']['total'] == 4
    assert get.json()['data']['items'][0]['id'] == auth_user_1['id']
    get = await client.get(f'/api/v1/admin/users', query_string={'username': 'user_2'})
    assert get.status_code == 200
    assert get.json()['data']['total'] == 1
    assert get.json()['data']['items'][0]['id'] == auth_user_2['id']
    get = await client.get(f'/api/v1/admin/users', query_string={'email': 'yandex'})
    assert get.status_code == 200
    assert get.json()['data']['total'] == 1
    assert get.json()['data']['items'][0]['id'] == auth_user_3['id']


async def users_for_test(client, mailhog, db_pool):
    token_1, auth_user_1, password_1 = await register_user(
        'user_1@mail.com',
        'user_1',
        'strong_password',
        client,
        mailhog)
    token_2, auth_user_2, password_2 = await register_user(
        'user_2@gmail.com',
        'user_2',
        'strong_password',
        client,
        mailhog)
    token_3, auth_user_3, password_3 = await register_user(
        'user_3@yandex.ru',
        'user_3',
        'strong_password',
        client,
        mailhog)
    token_4, auth_user_4, password_4 = await register_user(
        'user_4@ya.ru',
        'user_4',
        'strong_password',
        client,
        mailhog)
    await db_pool.execute(f'''INSERT INTO admin_users (user_id, en, ctime, atime, dtime)
                    VALUES ($1, $2, $3, $3, $3)''', *[auth_user_4['id'], True, datetime.datetime.now()])
    return auth_user_1, auth_user_2, auth_user_3, auth_user_4
