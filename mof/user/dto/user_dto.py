from typing import Annotated

from pydantic import EmailStr, Field, StrictStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from mof.abstract.dto import AbstractDTO
from mof.user.constants import RoleEnum


class UserDTO(AbstractDTO):
    email: Annotated[
        EmailStr,
        Field(
            alias="email",
            example="smith@ciatek.net",
            description="Required, user email, should be a valid not-empty string in email format."
        )
    ]
    first_name: Annotated[
        StrictStr,
        Field(
            alias="firstName",
            example="Mark",
            description="User first name, should be required, and valid.",
            min_length=1,
            max_length=50,
            pattern="^[a-zA-Z]*$",
        )
    ]
    last_name: Annotated[
        StrictStr,
        Field(
            alias="lastName",
            example="Smith",
            description="Required, last_name, should be a valid non-empty string less than 50 characters.",
            min_length=1,
            max_length=50,
            pattern="^[a-zA-Z]*$",
        )
    ]
    role: Annotated[
        RoleEnum,
        Field(
            alias="role",
            example="ADMINISTRATOR",
            description="Required, user role, should be one of the provided values."
        )
    ]
    phone: Annotated[
        PhoneNumber,
        Field(
            alias="phone",
            example="+374 55 55 55 55",
            description="Required, user phone, should be a valid not-empty string in phone number format, with max "
                        "length of 100 characters.",
            min_length=1,
            max_length=100
        )
    ]
    deactivated: Annotated[
        bool,
        Field(
            alias="deactivated",
            example=False,
            description="Required, user deactivated, should be a valid boolean."
        )
    ]
