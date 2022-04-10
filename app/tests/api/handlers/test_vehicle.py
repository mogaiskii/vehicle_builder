from aiohttp.test_utils import TestClient


async def test_smoke(api: TestClient) -> None:
    resp = await api.get('/vehicle/1')
    assert resp.status == 200 or resp.status == 404
