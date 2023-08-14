from typing import Annotated

from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError

from mof.exceptions import ErrorType, api_errors, dup_err_index, APIException
from mof.user.models.user_doc import UserIndexes


def user_unique_err_handle(e: DuplicateKeyError):
    index = dup_err_index(e)
    if index == UserIndexes.unique_email:
        raise APIException(user_errors.email_exists)
    elif index == UserIndexes.unique_phone:
        raise APIException(user_errors.phone_exists)
    else:
        raise e


class UserErrors(BaseModel):
    not_found: Annotated[
        ErrorType,
        Field(alias="notFound")
    ]
    email_exists: Annotated[
        ErrorType,
        Field(alias="emailExists")
    ]
    phone_exists: Annotated[
        ErrorType,
        Field(alias="phoneExists")
    ]
    invalid_password: Annotated[
        ErrorType,
        Field(alias="invalidPassword")
    ]


user_errors = UserErrors.model_validate(api_errors["user"])
