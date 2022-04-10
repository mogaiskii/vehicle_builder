__all__ = ('set_routes',)

from aiohttp import web
from api.handlers import VehicleView


def set_routes(app: web.Application) -> None:
    app.add_routes([
        web.get(r'/vehicle/{vehicle_id:\d+}', VehicleView)
    ])
