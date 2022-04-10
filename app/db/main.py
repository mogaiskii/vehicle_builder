from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


async def create_db_connection(url: str, debug: bool = False) -> AsyncEngine:
    return create_async_engine(
        url, echo=debug, pool_pre_ping=True
    )


async def close_db_connection(connection: AsyncEngine) -> None:
    await connection.dispose()
