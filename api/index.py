import logging
import sys
import time
import uuid

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

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


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc: HTTPException):
    logger.error(exc)
    return JSONResponse(content={"code": exc.status_code, "message": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc: RequestValidationError):
    logger.error(exc)
    valid_result = exc.args[0][0]
    message = valid_result["msg"]
    return JSONResponse(
        content=jsonable_encoder({"code": 400, "message": message}),
    )


@app.exception_handler(Exception)
async def base_exception_handler(_request, exc):
    logger.error(exc)
    return JSONResponse(content={"code": 500, "message": exc.detail})


@app.middleware("http")
async def log_requests(request, call_next):
    idem = str(uuid.uuid4()).replace('-', '')
    client_ip = await ip.get_client_ip(request)
    logger.info(f"ip={client_ip} - trace_id={idem} - start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"ip={client_ip} - trace_id={idem} - completed_in={formatted_process_time}ms, "
                f"status_code={response.status_code}")

    return response


app.include_router(qrcode.router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    return {"status": "alive"}
