from typing import Callable, Coroutine, Any

from aiohttp.test_utils import TestClient

from db.models import Vehicle


async def test_smoke(api: TestClient) -> None:
    resp = await api.get('/vehicle/1')
    assert resp.status == 200 or resp.status == 404


async def test_not_found(api: TestClient) -> None:
    resp = await api.get('/vehicle/0')
    assert resp.status == 404


async def test_simple_positive(
        api: TestClient,
        vehicle_generator: Callable[[], Coroutine[Any, Any, Vehicle]]
) -> None:
    vehicle = await vehicle_generator()
    resp = await api.get(f'/vehicle/{vehicle.id}')
    assert resp.status == 200
    body = await resp.json()
    assert body.get('id', vehicle.id)
    assert body.get('features')
    assert len(body.get('features')) == len(vehicle.vehicle_features)

    try:
        assert len(
            body.get('features')[0].get('functions')[0].get('components_ids')
        ) == len(
            vehicle.vehicle_features[0].vehicle_functions[0].vehicle_components
        )
    except AttributeError as e:
        assert False, e
