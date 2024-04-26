import logging
import sys
import time
import uuid

from fastapi import FastAPI

from api.router import qrcode
from utils import ip

logger = logging.getLogger()
logger.setLevel(logging.INFO)
console = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)

console.setFormatter(formatter)
logger.addHandler(console)  # 将日志输出至屏幕

logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def log_requests(request, call_next):
    idem = str(uuid.uuid4()).replace('-', '')
    client_ip = await ip.get_client_ip(request)
    logger.info(f"ip={client_ip} - trace_id={idem} - start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(
        f"ip={client_ip} - trace_id={idem} - completed_in={formatted_process_time}ms, status_code={response.status_code}")

    return response


app.include_router(qrcode.router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    return {"status": "alive"}
