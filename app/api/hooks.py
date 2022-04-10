from aiohttp.web import Application
from api.application import ApplicationHelper
from db.main import close_db_connection, create_db_connection


async def on_startup(app: Application) -> None:
    config = ApplicationHelper.get_config(app)
    database = await create_db_connection(config.db_url, config.debug)
    ApplicationHelper.set_database(app, database)


async def on_shutdown(app: Application) -> None:
    try:
        database = ApplicationHelper.get_database(app)
    except RuntimeError:
        return None

    await close_db_connection(database)
