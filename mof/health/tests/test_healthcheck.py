import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json.get("message") == "We're on the air."
