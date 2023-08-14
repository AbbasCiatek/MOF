from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError

from mof.exceptions import api_errors, ErrorType, APIException
from mof.exceptions import dup_err_index
from mof.firm.models.firm_doc import FirmIndexes


class FirmErrors(BaseModel):
    not_found: Annotated[
        ErrorType,
        Field(alias="notFound")
    ]
    name_exists: Annotated[
        ErrorType,
        Field(alias="nameExists")
    ]
    email_exists: Annotated[
        ErrorType,
        Field(alias="emailExists")
    ]
    phone_exists: Annotated[
        ErrorType,
        Field(alias="phoneExists")
    ]
    mof_exists: Annotated[
        ErrorType,
        Field(alias="mofExists")
    ]


firm_errors: FirmErrors = FirmErrors.model_validate(api_errors['firm'])


def firm_unique_err_handle(e: DuplicateKeyError):
    index = dup_err_index(e)
    if index == FirmIndexes.unique_name:
        raise APIException(firm_errors.name_exists)
    elif index == FirmIndexes.unique_email:
        raise APIException(firm_errors.email_exists)
    elif index == FirmIndexes.unique_phone:
        raise APIException(firm_errors.phone_exists)
    elif index == FirmIndexes.unique_mof:
        raise APIException(firm_errors.mof_exists)
    else:
        raise e
