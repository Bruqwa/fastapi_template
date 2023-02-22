import pytest
from httpx import AsyncClient


@pytest.fixture
async def mailhog():
    instance = MailHOG('http://mailhog:8025')
    await instance.clear()
    return instance


class MailHOG(object):
    def __init__(self, address):
        super().__init__()
        self._address = address

    async def clear(self):
        async with AsyncClient(base_url=self._address) as client:
            response = await client.delete('/api/v1/messages')
            assert response.status_code == 200

    async def messages(self):
        async with AsyncClient(base_url=self._address) as client:
            response = await client.get('/api/v1/messages')
            assert response.status_code == 200
            return response.json()

    async def message(self, message_id):
        async with AsyncClient(base_url=self._address) as client:
            response = await client.get(f'/api/v1/messages/{message_id}')
            assert response.status_code == 200
            return response.json()
