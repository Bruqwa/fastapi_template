import asyncio
import pytest
import logging
import datetime

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_goods(resetdb, client):
    good_1 = {
        'name': 'Potato',
        'description': 'Mc FREE'
    }
    good_2 = {
        'name': 'Tomato',
        'description': 'Red veg'
    }
    good_3 = {
        'name': 'Cucumber',
        'description': 'Green and fresh'
    }
    result_1 = await client.post('/api/v1/goods', json=good_1)
    assert result_1.status_code == 200, f'Status code error {result_1.text}'
    assert result_1.json()['data']['name'] == 'Potato'
    assert result_1.json()['data']['description'] == 'Mc FREE'

    result_2 = await client.post('/api/v1/goods', json=good_2)
    assert result_2.status_code == 200, f'Status code error {result_2.text}'
    assert result_2.json()['data']['name'] == 'Tomato'
    assert result_2.json()['data']['description'] == 'Red veg'

    result_3 = await client.post('/api/v1/goods', json=good_3)
    assert result_3.status_code == 200, f'Status code error {result_3.text}'
    assert result_3.json()['data']['name'] == 'Cucumber'
    assert result_3.json()['data']['description'] == 'Green and fresh'

    result_4 = await client.get('/api/v1/goods/all')
    assert result_4.status_code == 200
    assert result_4.json()['data']['total'] == 3
    assert result_4.json()['data']['page'] == 1


