import re
from urllib.parse import urlparse

import requests


def is_image(content_type: str) -> bool:
    """
    Checks if the given content type is an image or not.
    :param content_type: file mime type
    :return: bool
    """
    return content_type in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']


def is_image_url(url: str) -> bool:
    """
    根据链接的结尾或 header 中的 mime type 进行校验
    :param url: 文件 URL
    :return: bool
    """
    # 正则表达式用于匹配以常见图片文件扩展名结尾的 URL
    pattern = re.compile(r'\.(jpeg|jpg|png|gif|bmp|webp)$', re.IGNORECASE)
    # 只匹配 path ，避免 URL 中有参数导致校验不通过
    path = urlparse(url).path
    if re.search(pattern, path):
        return True
    mimetype = requests.head(url, allow_redirects=True).headers.get('content-type')
    return is_image(mimetype)


def is_url(url: str) -> bool:
    """
    校验是否是一个 URL，仅支持 http or https
    :param url: URL
    :return: bool
    """
    # URL正则
    pattern = re.compile(r'^(https?:\/\/)(www\.)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    return bool(re.match(pattern, url))
