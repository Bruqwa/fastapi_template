import pytest
from tests.fixtures.auth import (
    logout,
    confirm_code,
    get_code_from_mail,
)


@pytest.mark.asyncio
async def test_unauthorised_me(client, resetdb):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()['success'] is True

    assert response.json()['data']['token'] != ''
    assert response.json()['data']['me']['id'] == 0


@pytest.mark.asyncio
async def test_register_by_email(resetdb, user):
    pass


@pytest.mark.asyncio
async def test_register_and_me(client, resetdb, user):
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 200
    assert response.json()['success'] == True

    assert response.json()['data']['token'] == user['token']
    assert response.json()['data']['me'] == user['me']


@pytest.mark.asyncio
async def test_logout(resetdb, client, user):
    await logout(user['token'], client)


@pytest.mark.asyncio
async def test_recover(client, mailhog, resetdb, user):
    await logout(user['token'], client)
    await mailhog.clear()

    data = {
        'email': user['email']
    }
    response = await client.post("/api/v1/auth/recover", json=data)
    assert response.status_code == 200, f'response is {response.text}'

    code = await get_code_from_mail(user['email'], mailhog)

    await confirm_code(user['email'], code, client)


@pytest.mark.asyncio
async def test_login(client, resetdb, user):
    await logout(user['token'], client)

    data = {
        'email': user['email'],
        'password': user['password']
    }
    response = await client.post("/api/v1/auth/login", json=data)
    assert response.status_code == 200
    assert response.json()['data']['token'] == user['token']
    assert response.json()['data']['me'] == user['me']
