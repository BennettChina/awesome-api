import hashlib
import logging

from fastapi import APIRouter

from api.model.captcha import Captcha
from api.model.resp import ok
from modules.redis_client import redis_client
from utils.logger import logger

router = APIRouter()


@router.post("/manual/captcha", tags=["captcha"])
async def captcha(item: Captcha):
    """
    保存验证码结果
    :param item: 验证码通过的结果
    :return: None
    """
    key = f"{item.gt}:{item.geetest_challenge}"
    key = hashlib.md5(key.encode()).hexdigest()
    logger.info(f'key: {key}')
    redis_client.hset_all(key, item.__dict__)
    return ok()


@router.get("/manual/captcha", tags=["captcha"])
async def captcha_get(gt: str, challenge: str):
    """
    获取验证码的结果
    :param gt: gt
    :param challenge: challenge
    :return: see Captcha class
    """
    key = f"{gt}:{challenge}"
    key = hashlib.md5(key.encode()).hexdigest()
    logger.info(f'key: {key}')
    data = redis_client.hget_all(key)
    return ok(data)
