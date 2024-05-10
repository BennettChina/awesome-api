class R:
    def __init__(self, code: int, message: str, data=None):
        self.code = code
        self.message = message
        self.data = data


def ok(data=None):
    return R(0, 'success', data)


def error(code: int = None, message: str = None):
    if code is None:
        code = 1
    if message is None:
        message = "error"
    return R(code, message)
