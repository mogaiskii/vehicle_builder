import asyncio
from typing import Generator, Callable, Any, Coroutine

import pytest
from aiohttp import web
from aiohttp.web import Application
from aiohttp.test_utils import TestClient
from pytest_aiohttp.plugin import AiohttpClient  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from api.application import ApplicationHelper
from api.hooks import on_startup
from api.main import get_application
from db.models import Base, Vehicle, Component, Group, Feature, Function, FunctionComponent, VehicleFeatures, \
    VehicleFunctions, VehicleComponents, VehicleFunctionComponents
from db.queries.vehicles import get_vehicle
from settings import Settings


@pytest.fixture
def settings() -> Settings:
    settings = Settings(db_url='')
    settings.db_url = settings.test_db_url
    return settings


async def init_db(app: web.Application) -> None:
    engine = ApplicationHelper.get_database(app)
    meta = Base.metadata

    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


@pytest.fixture
def app(event_loop: asyncio.AbstractEventLoop, settings: Settings) -> Generator[Application, None, None]:
    app = get_application(settings=settings, skip_checks=True)
    event_loop.run_until_complete(on_startup(app))
    event_loop.run_until_complete(init_db(app))
    yield app
    event_loop.run_until_complete(app.shutdown())


@pytest.fixture
def api(
        event_loop: asyncio.AbstractEventLoop,
        aiohttp_client: AiohttpClient,
        app: Application,
) -> Generator[TestClient, None, None]:
    yield event_loop.run_until_complete(aiohttp_client(app))


@pytest.fixture
def session(app: Application) -> AsyncSession:
    return ApplicationHelper.get_session(app)


@pytest.fixture
def vehicle_generator(session: AsyncSession) -> Callable[[], Coroutine[Any, Any, Vehicle]]:
    async def generator() -> Vehicle:
        async with session:
            component = Component(name='component', cad_model_url='url')
            session.add(component)

            group = Group(name='group')
            session.add(group)
            await session.flush()

            feature = Feature(name='feature', group_id=group.id)
            session.add(feature)
            await session.flush()

            function = Function(name='function', feature_id=feature.id)
            session.add(function)
            await session.flush()

            function_component = FunctionComponent(function_id=function.id, component_id=component.id)
            session.add(function_component)

            vehicle = Vehicle(name='vehicle')
            session.add(vehicle)
            await session.flush()

            vehicle_feature = VehicleFeatures(vehicle_id=vehicle.id, feature_id=feature.id)
            session.add(vehicle_feature)
            await session.flush()

            vehicle_function = VehicleFunctions(function_id=function.id, vehicle_feature_id=vehicle_feature.id)
            session.add(vehicle_function)
            await session.flush()

            vehicle_component = VehicleComponents(vehicle_id=vehicle.id, component_id=component.id, component_amount=5)
            session.add(vehicle_component)
            await session.flush()

            vehicle_function_component = VehicleFunctionComponents(
                vehicle_function_id=vehicle_function.id,
                vehicle_component_id=vehicle_component.id
            )
            session.add(vehicle_function_component)

            await session.commit()

            assert type(vehicle.id) == int  # mypy
            vehicle = await get_vehicle(session, vehicle.id)
        return vehicle
    return generator
