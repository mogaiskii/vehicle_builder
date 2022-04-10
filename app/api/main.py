from aiohttp.web import Application
from api.application import ApplicationHelper
from api.hooks import on_shutdown, on_startup
from api.routes import set_routes
from settings import Settings


def get_application(settings: Settings = None, skip_checks: bool = False) -> Application:
    if settings is None:
        settings = Settings()

    app = Application()
    ApplicationHelper.set_config(app, settings)

    set_routes(app)

    app.on_startup.append(on_startup)  # type: ignore
    app.on_shutdown.append(on_shutdown)  # type: ignore

    if not skip_checks:
        app.on_startup.append(ApplicationHelper.init_check)  # type: ignore

    return app
