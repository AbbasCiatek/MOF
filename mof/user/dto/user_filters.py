from typing import Annotated

from fastapi import Query
from pydantic import EmailStr, StrictStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from mof.abstract.filters import AbstractFilters
from mof.user.constants import RoleEnum


class UserFilters(AbstractFilters):
    email: Annotated[
        EmailStr | None,
        Query(
            alias="email",
            examples=["asrour@ciatek.net"],
            description="User email, should be a valid not-empty string in email format.",
            min_length=1,
            max_length=480
        )
    ] = None
    first_name: Annotated[
        StrictStr | None,
        Query(
            alias="firstName",
            examples=["Mark"],
            description="User first name, should be a valid non-empty string less than 50 characters.",
            min_length=1,
            max_length=50,
            pattern="^[a-zA-Z]*$",
        )
    ] = None
    last_name: Annotated[
        StrictStr | None,
        Query(
            alias="lastName",
            examples=["Smith"],
            description="User last name, should be a valid non-empty string less than 50 characters.",
            min_length=1,
            max_length=50,
            pattern="^[a-zA-Z]*$",
        )
    ] = None
    role: Annotated[
        RoleEnum | None,
        Query(
            alias="role",
            examples=["ADMINISTRATOR"],
            description="User role, should be one of the provided values.",
            min_length=1,
            max_length=50
        )
    ] = None
    phone: Annotated[
        PhoneNumber | None,
        Query(
            alias="phone",
            examples=["+374 55 55 55 55"],
            description="Required, user phone, should be a valid not-empty string in phone number format, with max "
                        "length of 100 characters.",
            min_length=1,
            max_length=100
        )
    ] = None
