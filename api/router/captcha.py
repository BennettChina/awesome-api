from fastapi import APIRouter

from api.model.captcha import Captcha, CaptchaV4
from api.model.resp import ok, error
from modules.redis_client import redis_client

router = APIRouter()


@router.post("/manual/captcha", tags=["captcha"])
async def captcha(item: Captcha):
    """
    保存验证码结果
    :param item: 验证码通过的结果，支持极验 V3 或 V4
    :return: None
    """
    if isinstance(item, CaptchaV4):
        key = item.captcha_id
        value = item.model_dump()
    else:
        key = item.geetest_challenge
        value = item.model_dump()

    redis_client.hset_all(key, value)
    # 缓存验证结果 10 分钟
    redis_client.expire(key, 600)
    return ok()


@router.get("/manual/captcha", tags=["captcha"])
async def captcha_get(challenge: str):
    """
    获取验证码的结果
    :param challenge: 极验 V3 的 geetest_challenge，或极验 V4 的 captcha_id
    :return: see Captcha class
    """
    data = redis_client.hget_all(challenge)
    if data.__len__() == 0:
        return error(1404, "not found challenge")
    return ok(data)
