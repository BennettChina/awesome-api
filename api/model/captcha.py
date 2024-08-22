from pydantic import BaseModel


class Captcha(BaseModel):
    geetest_challenge: str
    geetest_validate: str
    geetest_seccode: str
