from pydantic import BaseSettings


class Settings(BaseSettings):
    db_url: str
    test_db_url: str = ''
    debug: bool = False
