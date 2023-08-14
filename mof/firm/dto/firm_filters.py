from typing import Annotated

from fastapi import Query
from pydantic import EmailStr, StrictStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from mof.abstract.filters import AbstractFilters


class FirmFilters(AbstractFilters):
    email: Annotated[
        EmailStr | None,
        Query(
            alias="email",
            description="Email of the firm",
            example="somefirm@somedomain.someextension",
            min_length=1,
            max_length=480,
        )
    ] = None
    name: Annotated[
        StrictStr | None,
        Query(
            alias="name",
            description="Name of the firm",
            example="Firm name",
            min_length=1,
            max_length=255,
        )
    ] = None
    phone: Annotated[
        PhoneNumber | None,
        Query(
            alias="phone",
            description="Phone number of the firm",
            example="+380123456789",
            min_length=1,
            max_length=255,
        )
    ] = None
    mof: Annotated[
        StrictStr | None,
        Query(
            alias="mof",
            description="Mof of the firm",
            example="12345678",
            min_length=1,
            max_length=255,
        )
    ] = None
