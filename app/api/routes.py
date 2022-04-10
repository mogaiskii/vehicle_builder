__all__ = ('set_routes',)

from aiohttp import web
from api.handlers import get_vehicle


def set_routes(app: web.Application) -> None:
    app.add_routes([
        web.get(r'/vehicle/{vehicle_id:\d+}', get_vehicle)
    ])
