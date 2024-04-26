from fastapi import APIRouter, HTTPException, UploadFile

from modules import decode_qrcode
from utils import fetch, validate

router = APIRouter()


@router.post("/qrcode", tags=["qrcode"])
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
    return res


@router.get("/qrcode", tags=["qrcode"])
async def qrcode(url: str):
    """
    解析图片中二维码的内容
    :param url: 图片的 URL
    :return: 解析结果数组
    """
    if len(url) == 0 or not validate.is_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    if not validate.is_image_url(url):
        raise HTTPException(status_code=400, detail="File type not supported")
    img = await fetch.download_file(url)
    res, _ = await decode_qrcode.decode(img)
    return res
