import time
import uuid
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from api.model.resp import error
from api.router import *
from modules.redis_client import redis_client
from utils import ip
from utils.logger import logger


@asynccontextmanager
async def register_redis(_app: FastAPI):
    redis_client.connect()
    logger.info('Connected to Redis')
    yield
    redis_client.disconnect()
    logger.info('Disconnected from Redis')


app = FastAPI(lifespan=register_redis)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request, exc: HTTPException):
    logger.exception(exc, exc_info=False)
    return JSONResponse(content={"code": exc.status_code, "message": exc.detail})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request, exc: RequestValidationError):
    logger.exception(exc, exc_info=False)
    valid_result = exc.args[0][0]
    message = valid_result["msg"]
    return JSONResponse(
        content=jsonable_encoder(error(400, message)),
    )


@app.exception_handler(Exception)
async def base_exception_handler(_request, exc: Exception):
    logger.exception(exc)
    return JSONResponse(content=jsonable_encoder(error(500, "未知异常")))


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = str(uuid.uuid4()).replace('-', '')
    client_ip = await ip.get_client_ip(request)
    body = ""
    if request.headers.get("Content-Type") == "application/x-www-form-urlencoded":
        body = await request.form()
    if request.headers.get("Content-Type") == "application/json":
        body = await request.json()
    query_params = dict(request.query_params)
    logger.info(f"ip={client_ip} - trace_id={idem} - start request path={request.url.path}, "
                f"query_params={query_params}, body={body}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    response_body = ""
    content_type = response.headers.get("content-type", "")
    if content_type.startswith("application/json"):
        body_iterator = getattr(response, "body_iterator", None)
        if body_iterator is not None:
            body_bytes = b"".join([chunk async for chunk in body_iterator])
            response = Response(
                content=body_bytes,
                status_code=response.status_code,
                headers=dict(response.headers),
                background=response.background,
            )
            try:
                response_body = json.loads(body_bytes)
            except (json.JSONDecodeError, UnicodeDecodeError):
                response_body = body_bytes.decode("utf-8", errors="replace")
    logger.info(f"ip={client_ip} - trace_id={idem} - completed_in={formatted_process_time}ms, "
                f"status_code={response.status_code}, response={response_body}")

    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(qrcode_router, prefix="/api", tags=["api"])
app.include_router(captcha_router, prefix="/api", tags=["api"])


@app.get("/")
async def root():
    return {"status": "alive"}
