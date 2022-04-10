import asyncio
from typing import Generator

import pytest
from aiohttp.test_utils import TestClient
from api.application import get_application
from pytest_aiohttp.plugin import AiohttpClient  # type: ignore


@pytest.fixture
def api(event_loop: asyncio.AbstractEventLoop, aiohttp_client: AiohttpClient) -> Generator[TestClient, None, None]:
    app = get_application()
    yield event_loop.run_until_complete(aiohttp_client(app))
    event_loop.run_until_complete(app.shutdown())
