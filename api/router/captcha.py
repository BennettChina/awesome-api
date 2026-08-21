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
        key = item.key or item.captcha_id
    else:
        key = item.key or item.geetest_challenge
    value = item.model_dump(exclude={"key"})

    redis_client.hset_all(key, value)
    # 缓存验证结果 10 分钟
    redis_client.expire(key, 600)
    return ok()


@router.get("/manual/captcha", tags=["captcha"])
async def captcha_get(challenge: str | None = None, key: str | None = None):
    """
    获取验证码的结果
    :param challenge: 兼容旧参数，传入缓存键即可
    :param key: 新增的缓存键
    :return: see Captcha class
    """
    cache_key = key or challenge
    if not cache_key:
        return error(400, "missing key or challenge")
    data = redis_client.hget_all(cache_key)
    if data.__len__() == 0:
        return error(1404, "not found challenge")
    return ok(data)
