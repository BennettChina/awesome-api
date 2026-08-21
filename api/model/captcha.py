from typing import Union

from pydantic import BaseModel


class CaptchaV3(BaseModel):
    key: str | None = None
    geetest_challenge: str
    geetest_validate: str
    geetest_seccode: str


class CaptchaV4(BaseModel):
    key: str | None = None
    captcha_id: str
    lot_number: str
    pass_token: str
    gen_time: str
    captcha_output: str


Captcha = Union[CaptchaV3, CaptchaV4]
