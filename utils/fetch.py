import logging

import httpx
from fastapi import HTTPException


async def download_file(url: str, headers: dict | None, timeout: int) -> bytes:
    response = httpx.get(url, timeout=timeout, headers=headers)
    if response.status_code != 200:
        logging.info(response.text)
        raise HTTPException(400, f"URL 不可用，访问结果为{response.status_code}")
    return bytearray(response.content)


async def get(url, params, headers):
    response = httpx.get(url, params=params, headers=headers)
    return response


async def post(url, params, headers):
    response = httpx.post(url, params=params, headers=headers)
    return response
