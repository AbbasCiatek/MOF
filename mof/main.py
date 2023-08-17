import os
import time
from typing import Any, Callable

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.requests import Request

from mof import __project_id__, __version__
from mof.database import start_async_mongodb
from mof.exceptions import APIException, api_exception_handler
from mof.routes import get_routes
from mof.apienv import apienv

os.environ["TZ"] = "UTC"

#
#   create the api
#
api = FastAPI(title=f"MOF Backend: {__project_id__}", version=__version__)
add_pagination(api)
api.add_exception_handler(APIException, api_exception_handler)


#
#   middleware
#
@api.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable) -> Any:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@api.on_event("startup")
async def startup_event():
    print(apienv)
    # db = await start_async_mongodb()
    # api.db = db


#
#   set routers
#
get_routes(api)
