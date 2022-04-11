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
from db.models import Base, Vehicle
from db.queries.vehicles import get_vehicle
from settings import Settings
from tests.utils import build_vehicle


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
            vehicle = await build_vehicle(session)

            await session.commit()

            assert type(vehicle.id) == int  # mypy
            vehicle = await get_vehicle(session, vehicle.id)
        return vehicle
    return generator
