import requests
from fastapi import HTTPException


async def download_file(url: str) -> bytes:
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(400, f"URL 不可用，访问结果为{response.status_code}")
    return bytearray(response.content)


async def get(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    return response


async def post(url, params, headers):
    response = requests.post(url, params=params, headers=headers)
    return response
