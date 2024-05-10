from fastapi import APIRouter, HTTPException, UploadFile

from api.model.net_resource import NetResource
from api.model.resp import ok
from modules import decode_qrcode
from utils import fetch, validate

router = APIRouter()


@router.post("/qrcode/file", tags=["qrcode"])
async def qrcode_file(file: UploadFile):
    """
    解析图片中二维码的内容
    :param file: 图片文件
    :return: 解析结果数组
    """
    if not validate.is_image(file.content_type):
        raise HTTPException(status_code=400, detail="File type not supported")
    if file.size == 0:
        raise HTTPException(status_code=400, detail="Empty File")
    img = await file.read(file.size)
    res, _ = await decode_qrcode.decode(img)
    await file.close()
    return ok(res)


@router.post("/qrcode/url", tags=["qrcode"])
async def qrcode(item: NetResource):
    """
    解析图片中二维码的内容
    :param item: 下载图片使用的参数
    :return: 解析结果数组
    """
    url = item.url
    if len(url) == 0 or not validate.is_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    img = await fetch.download_file(url, item.headers, item.timeout)
    res, _ = await decode_qrcode.decode(img)
    return ok(res)
