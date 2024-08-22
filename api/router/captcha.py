from fastapi import APIRouter

from api.model.captcha import Captcha
from api.model.resp import ok, error
from modules.redis_client import redis_client

router = APIRouter()


@router.post("/manual/captcha", tags=["captcha"])
async def captcha(item: Captcha):
    """
    保存验证码结果
    :param item: 验证码通过的结果
    :return: None
    """
    redis_client.hset_all(item.geetest_challenge, item.__dict__)
    # 缓存验证结果 10 分钟
    redis_client.expire(item.geetest_challenge, 600)
    return ok()


@router.get("/manual/captcha", tags=["captcha"])
async def captcha_get(challenge: str):
    """
    获取验证码的结果
    :param challenge: challenge
    :return: see Captcha class
    """
    data = redis_client.hget_all(challenge)
    if data.__len__() == 0:
        return error(1401, "invalid params")
    return ok(data)
