from typing import Optional

from aiohttp import web
from aiohttp_pydantic import PydanticView  # type: ignore
from settings import Settings
from sqlalchemy import literal, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


class ApplicationHelper:
    @staticmethod
    def get_config(application: web.Application) -> Settings:
        settings: Optional[Settings] = application.get('config', None)
        if settings is None:
            raise RuntimeError('Improperly configured. Settings must be set!')

        return settings

    @staticmethod
    def set_config(application: web.Application, config: Settings) -> None:
        application['config'] = config

    @staticmethod
    def get_database(application: web.Application) -> AsyncEngine:
        db: Optional[AsyncEngine] = application.get('database', None)
        if db is None:
            raise RuntimeError('Improperly configured. Database must be set!')

        return db

    @staticmethod
    def set_database(application: web.Application, database: AsyncEngine) -> None:
        application['database'] = database
        application['sessionmaker'] = sessionmaker(
            database, expire_on_commit=False, class_=AsyncSession
        )

    @staticmethod
    def get_session(application: web.Application) -> AsyncSession:
        maker: Optional[sessionmaker] = application.get('sessionmaker', None)
        if maker is None:
            raise RuntimeError('Improperly configured. Database must be set!')

        return maker()

    @classmethod
    async def init_check(cls, application: web.Application) -> None:
        if cls.get_config(application) and cls.get_database(application):
            async with cls.get_session(application) as session:
                await session.execute(select(literal(0)))


class RequestHandler(PydanticView):
    @property
    def config(self) -> Settings:
        return ApplicationHelper.get_config(self.request.app)

    @property
    def database(self) -> AsyncEngine:
        return ApplicationHelper.get_database(self.request.app)

    def get_session(self) -> AsyncSession:
        return ApplicationHelper.get_session(self.request.app)
