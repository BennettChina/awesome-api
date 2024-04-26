import requests


async def download_file(url: str) -> bytes:
    response = requests.get(url)
    return bytearray(response.content)


async def get(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    return response


async def post(url, params, headers):
    response = requests.post(url, params=params, headers=headers)
    return response
