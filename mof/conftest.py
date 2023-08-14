import asyncio
from typing import Iterator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from starlette.config import environ

from mof.main import api

environ["TESTING"] = "True"


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    pending = asyncio.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
    loop.close()
    asyncio.set_event_loop(None)


@pytest.fixture()
async def client() -> Iterator[AsyncClient]:
    async with LifespanManager(api):
        async with AsyncClient(app=api, base_url="http://test", follow_redirects=True) as _client:
            try:
                yield _client
            except Exception as exc:
                print(exc)
            finally:
                await clear_database(api)


async def clear_database(api: FastAPI) -> None:
    """Empties the test database"""
    for collection in await api.db.list_collections():
        await api.db[collection["name"]].delete_many({})
