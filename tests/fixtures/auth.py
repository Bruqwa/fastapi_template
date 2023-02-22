import pytest
import base64
import re
from typing import Tuple


@pytest.fixture
async def user(
        client,
        mailhog
) -> dict:
    email = 'test@mail.ru'
    username = 'TestUser'
    password = 'strong_password'
    token, user, password = await register_user(
        email,
        username,
        password,
        client,
        mailhog,
    )
    return {
        'token': token,
        'me': user,
        'password': password,
        'email': email
    }


async def register_user(
        email,
        username,
        password,
        client,
        mailhog,
) -> Tuple[str, dict, str]:
    data = {
        'email': email,
        'name': username,
        'password': password,

    }
    response = await client.post("/api/v1/auth/register", json=data)
    assert response.status_code == 200, f'status_code={response.status_code}, reponse={response.text}'

    code = await get_code_from_mail(email, mailhog)

    token, user = await confirm_code(email, code, client)

    return token, user, password


async def get_code_from_mail(email, mailhog):
    messages = await mailhog.messages()
    if len(messages) == 1:
        assert len(messages) == 1
    elif len(messages) == 3:
        assert len(messages) == 3

    message = messages[0]
    assert email in message['Content']['Headers']['To']
    body = base64.decodebytes(bytes(message['MIME']['Parts'][0]['Body'], 'utf8')).decode('utf-8')
    result = re.search(r'[0-9]{4,}', body)
    return int(result.group(0))


async def get_password_from_mail(email, mailhog):
    messages = await mailhog.messages()

    message = messages[0]
    assert email in message['Content']['Headers']['To']
    body = base64.decodebytes(bytes(message['MIME']['Parts'][0]['Body'], 'utf8')).decode('utf-8')
    result = re.search(r'Ваш новый постоянный пароль <b>([0-9a-zA-Z]{8,12})</b>', body)
    return result.group(1)


async def confirm_code(email, code, client):
    data = {
        'email': email,
        'code': code
    }
    response = await client.post("/api/v1/auth/confirm", json=data)
    assert response.status_code == 200, f'code={code}, response={response.text}'
    assert response.json()['data']['token'] != ''
    assert response.json()['data']['me']['id'] != 0, f'wrong confirm data {response.json()}'

    return response.json()['data']['token'], response.json()['data']['me']


async def logout(token, client):
    response = await client.post("/api/v1/auth/logout")
    assert response.status_code == 200, response.text
    assert response.json()['success'] == True

    assert response.json()['data']['token'] == token
    assert response.json()['data']['me']['id'] == 0
