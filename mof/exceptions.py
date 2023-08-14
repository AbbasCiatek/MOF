import json
import re
from typing import Annotated
from urllib.request import Request

from fastapi import HTTPException
from pydantic import BaseModel, Field, ConfigDict
from pymongo.errors import DuplicateKeyError
from starlette.responses import JSONResponse


class ErrorType(BaseModel):
    status_code: Annotated[
        int,
        Field(
            alias="statusCode",
        )
    ]
    message: Annotated[
        str,
        Field(
            alias="message",
        )
    ]
    code: Annotated[
        str,
        Field(
            alias="code",
        )
    ]
    context: [
        dict | None,
        Field(
            alias="context",
        )
    ] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)


class APIException(HTTPException):
    code: str = None
    context: dict | None = None
    message: str = None

    def __init__(self, error: ErrorType, headers: dict | None = None):
        super().__init__(error.status_code, detail=error.message, headers=headers)
        self.code = error.code
        self.context = error.context
        self.message = error.message


def api_exception_handler(request: Request, exc: APIException):
    content = {}

    if exc.message:
        content["message"] = exc.message if exc.message else exc.detail

    if exc.code:
        content["code"] = exc.code

    if exc.context:
        content["context"] = exc.context

    return JSONResponse(status_code=exc.status_code, content=content)


def load_errors(module: str | None = None) -> dict[str, dict]:
    with open('mof/errorCodes.json') as json_file:
        if module:
            return json.load(json_file)[module]
        return json.load(json_file)


api_errors = load_errors()


def dup_err_index(error: DuplicateKeyError) -> str | None:
    error_msg = error.details["errmsg"]
    regex = r"index: (\w+)"
    matches = re.search(regex, error_msg)
    if matches:
        return matches.group(1)
