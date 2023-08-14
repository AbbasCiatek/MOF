from enum import Enum
from typing import Annotated

import pymongo
from pydantic import StrictStr, Field, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from pymongo import IndexModel

from mof.abstract.model import AbstractDocument


class FirmIndexes(str, Enum):
    unique_name = "firm_unique_name"
    unique_email = "firm_unique_email"
    unique_phone = "firm_unique_phone"
    unique_mof = "firm_unique_mof"
    firm_search = "firm_search"


class Address(BaseModel):
    unit: Annotated[
        str | None,
        Field(
            alias="unit",
            description="Unit of the firm",
            example="Unit name",
            min_length=1,
            max_length=255,
        )
    ] = None
    building: Annotated[
        StrictStr,
        Field(
            alias="building",
            description="Building of the firm",
            example="Building name",
            min_length=1,
            max_length=255,
        )
    ]
    street: Annotated[
        StrictStr,
        Field(
            alias="street",
            description="Street of the firm",
            example="Street name",
            min_length=1,
            max_length=255,
        )
    ]
    postal_code: Annotated[
        StrictStr,
        Field(
            alias="postalCode",
            description="Postal code of the firm",
            example="Postal code",
            min_length=1,
            max_length=255,
        )
    ]
    city: Annotated[
        StrictStr,
        Field(
            alias="city",
            description="City of the firm",
            example="City name",
            min_length=1,
            max_length=255,
        )
    ]
    sub_region: Annotated[
        StrictStr,
        Field(
            alias="subRegion",
            description="Sub region of the firm",
            example="Sub region name",
            min_length=1,
            max_length=255,
        )
    ]
    region: Annotated[
        StrictStr,
        Field(
            alias="region",
            description="Region of the firm",
            example="Region name",
            min_length=1,
            max_length=255,
        )
    ]
    country_of_origin: Annotated[
        StrictStr | None,
        Field(
            alias="countryOfOrigin",
            description="Country of origin of the firm",
            example="Country of origin name",
            min_length=1,
            max_length=255,
        )
    ]


class FirmDocument(AbstractDocument):
    name: Annotated[
        StrictStr,
        Field(
            alias="name",
            description="Name of the firm",
            example="Firm name",
            min_length=1,
            max_length=255,
        )
    ]
    phone: Annotated[
        PhoneNumber,
        Field(
            alias="phone",
            description="Phone number of the firm",
            example="+380123456789",
        )
    ]
    mof: Annotated[
        StrictStr,
        Field(
            alias="mof",
            description="Mof of the firm",
            example="12345678",
            min_length=1,
            max_length=255,
        )
    ]
    email: Annotated[
        EmailStr,
        Field(
            alias="email",
            description="Email of the firm",
            example="somefirm@somedomain.someextension"
        )
    ]
    address: Annotated[
        Address,
        Field(
            alias="address",
            description="Address of the firm",
        )
    ]

    class Settings:
        name = "firm"
        use_revision = True
        indexes = [
            IndexModel([("name", pymongo.ASCENDING)], unique=True, name=FirmIndexes.unique_name),
            IndexModel([("email", pymongo.ASCENDING)], unique=True, name=FirmIndexes.unique_email),
            IndexModel([("phone", pymongo.ASCENDING)], unique=True, name=FirmIndexes.unique_phone),
            IndexModel([("mof", pymongo.ASCENDING)], unique=True, name=FirmIndexes.unique_mof),
            IndexModel([
                ("name", pymongo.TEXT),
                ("email", pymongo.TEXT),
                ("phone", pymongo.TEXT),
                ("mof", pymongo.TEXT),
            ], name=FirmIndexes.firm_search)
        ]
