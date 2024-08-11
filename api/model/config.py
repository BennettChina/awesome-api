from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str = None
    redis_db: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
