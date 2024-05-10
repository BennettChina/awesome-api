import re


def is_image(content_type: str) -> bool:
    """
    Checks if the given content type is an image or not.
    :param content_type: file mime type
    :return: bool
    """
    return content_type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']


def is_url(url: str) -> bool:
    """
    校验是否是一个 URL，仅支持 http or https
    :param url: URL
    :return: bool
    """
    # URL正则
    pattern = re.compile(r'^(https?:\/\/)(www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    return bool(re.match(pattern, url))
