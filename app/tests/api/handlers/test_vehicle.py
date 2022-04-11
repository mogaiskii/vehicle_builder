from typing import Callable, Coroutine, Any

from aiohttp.test_utils import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Vehicle
from db.queries.vehicles import get_vehicle
from tests.utils import create_function, create_component, bind_function_component, bind_vehicle_function, \
    bind_vehicle_component, bind_vehicle_function_component


async def test_smoke(api: TestClient) -> None:
    resp = await api.get('/vehicle/1')
    assert resp.status == 200 or resp.status == 404


async def test_not_found(api: TestClient) -> None:
    resp = await api.get('/vehicle/0')
    assert resp.status == 404


async def test_incorrect(api: TestClient) -> None:
    resp = await api.get('/vehicle/a')
    assert resp.status == 404

    resp = await api.get('/vehicle/[]')
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


async def test_get_correct_vehicle_from_multiple(
        api: TestClient, vehicle_generator: Callable[[], Coroutine[Any, Any, Vehicle]]
) -> None:
    await vehicle_generator()
    vehicle = await vehicle_generator()
    await vehicle_generator()

    resp = await api.get(f'/vehicle/{vehicle.id}')
    assert resp.status == 200
    body = await resp.json()
    assert body.get('id', vehicle.id)
    assert body.get('features')
    assert len(body.get('features')) == len(vehicle.vehicle_features)
    assert body.get('features')[0].get('id') == vehicle.vehicle_features[0].feature_id


async def test_manytomany_components(
        api: TestClient,
        vehicle_generator: Callable[[], Coroutine[Any, Any, Vehicle]],
        session: AsyncSession
) -> None:
    vehicle = await vehicle_generator()
    vehicle_feature = vehicle.vehicle_features[0]
    function_1 = vehicle_feature.vehicle_functions[0].function
    component_1 = vehicle_feature.vehicle_functions[0].vehicle_components[0].component
    async with session:
        function_2 = await create_function(session, vehicle_feature.feature_id)
        component_2 = await create_component(session)

        await bind_vehicle_function(session, function_2.id, vehicle_feature.id)
        await bind_vehicle_component(session, vehicle.id, component_2.id)

        await bind_function_component(session, function_2.id, component_2.id)
        await bind_vehicle_function_component(session, function_2.id, component_2.id)

        await bind_function_component(session, function_1.id, component_2.id)
        await bind_vehicle_function_component(session, function_1.id, component_2.id)

        await bind_function_component(session, function_2.id, component_1.id)
        await bind_vehicle_function_component(session, function_2.id, component_1.id)

        await session.commit()

    assert vehicle.id  # mypy
    vehicle = await get_vehicle(session, vehicle.id)

    resp = await api.get(f'/vehicle/{vehicle.id}')
    assert resp.status == 200
    body = await resp.json()
    assert body.get('id', vehicle.id)

    try:
        assert len(
            body.get('features')[0].get('functions')[0].get('components_ids')
        ) == 2
        assert set(
            body.get('features')[0].get('functions')[0].get('components_ids')
        ) == {component_1.id, component_2.id}

        assert set(
            body.get('features')[0].get('functions')[1].get('components_ids')
        ) == {component_1.id, component_2.id}
    except AttributeError as e:
        assert False, e
