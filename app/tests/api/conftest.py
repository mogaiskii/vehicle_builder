import asyncio
from typing import Generator

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from pytest_aiohttp.plugin import AiohttpClient  # type: ignore

from api.application import ApplicationHelper
from api.hooks import on_startup
from api.main import get_application
from db.models import Base
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
def api(
        event_loop: asyncio.AbstractEventLoop,
        aiohttp_client: AiohttpClient,
        settings: Settings
) -> Generator[TestClient, None, None]:
    app = get_application(settings=settings, skip_checks=True)
    event_loop.run_until_complete(on_startup(app))
    event_loop.run_until_complete(init_db(app))
    yield event_loop.run_until_complete(aiohttp_client(app))
    event_loop.run_until_complete(app.shutdown())
