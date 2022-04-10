from aiohttp import web
from api.hooks import on_shutdown, on_startup
from api.routes import set_routes


def get_application() -> web.Application:
    app = web.Application()
    set_routes(app)

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app
