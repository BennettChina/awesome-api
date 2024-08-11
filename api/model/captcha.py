from pydantic import BaseModel


class Captcha(BaseModel):
    gt: str
    geetest_challenge: str
    geetest_validate: str
    geetest_seccode: str
