from typing import Any

from aiohttp import web
from api.main import get_application


def init_app(argv: Any = None) -> web.Application:
    return get_application()


if __name__ == '__main__':
    web.run_app(get_application())
