from pydantic import BaseModel


class NetResource(BaseModel):
    url: str
    headers: dict | None = None
    timeout: int | None = 60
