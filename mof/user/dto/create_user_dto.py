from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StrictStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from mof.auth.utils import check_password_secure
from mof.exceptions import APIException
from mof.user.constants import RoleEnum
from mof.user.errors import user_errors


class CreateUserDTO(BaseModel):
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
    password: Annotated[
        StrictStr,
        Field(
            alias="password",
            example="Ciatek@123",
            description="Required, user password, should be a valid not-empty string. should have at least 8"
                        "characters, at least one uppercase letter, one lowercase letter, one number and one special "
                        "character, and should not exceed 32 characters.",
        )
    ]

    @field_validator("password")
    def validate_password(cls, value: str):
        secure = check_password_secure(value)
        if not secure:
            raise APIException(user_errors.invalid_password)
        return value
