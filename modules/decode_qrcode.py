import cv2
import numpy as np


async def decode(image: bytes):
    detector = cv2.wechat_qrcode.WeChatQRCode("model/detect.prototxt", "model/detect.caffemodel", "model/sr.prototxt",
                                              "model/sr.caffemodel")
    buffer = np.frombuffer(image, dtype=np.uint8)
    img = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    return detector.detectAndDecode(img)
