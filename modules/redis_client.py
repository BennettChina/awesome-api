import redis

from api.model.config import Config


class RedisClient:
    host = str
    port = int
    db = int
    password = str | None
    client: redis.Redis | None = None

    def __init__(self):
        config = Config()
        self.host = config.redis_host
        self.port = config.redis_port
        self.password = config.redis_password
        self.db = config.redis_db
        self.client = None

    def connect(self):
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password,
                                  decode_responses=True)

    def disconnect(self):
        if self.client:
            self.client.close()

    def get(self, key: str) -> str:
        return self.client.get(key)

    def set(self, key: str, value: str) -> None:
        self.client.set(key, value)

    def set_with_timeout(self, key: str, value: str, timeout: int) -> None:
        self.client.set(key, value, timeout)

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def expire(self, key: str, timeout: int) -> None:
        self.client.expire(key, timeout)

    def hset(self, key: str, hash_key: str, value: str) -> None:
        self.client.hset(key, hash_key, value)

    def hset_all(self, key: str, value: dict) -> None:
        self.client.hset(name=key, mapping=value)

    def hget(self, key: str, hash_key: str) -> str | None:
        return self.client.hget(key, hash_key)

    def hget_all(self, key: str) -> dict:
        return self.client.hgetall(key)

    def hdel(self, key: str) -> None:
        self.client.hdel(key)


redis_client = RedisClient()
__all__ = ["redis_client"]
