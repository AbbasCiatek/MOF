from typing import Annotated

from pydantic import BaseModel, StrictStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from mof.user.constants import RoleEnum


class UpdateUserDTO(BaseModel):
    first_name: Annotated[
        StrictStr | None,
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
        StrictStr | None,
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
        RoleEnum | None,
        Field(
            alias="role",
            example="ADMINISTRATOR",
            description="Required, user role, should be one of the provided values."
        )
    ]
    phone: Annotated[
        PhoneNumber | None,
        Field(
            alias="phone",
            example="+374 55 55 55 55",
            description="Required, user phone, should be a valid not-empty string in phone number format, with max "
                        "length of 100 characters.",
            min_length=1,
            max_length=100
        )
    ]
