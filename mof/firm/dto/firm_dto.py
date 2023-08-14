from typing import Annotated

from pydantic import BaseModel, Field, StrictStr, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from mof.abstract.dto import AbstractDTO


class AddressDTO(BaseModel):
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


class FirmDTO(AbstractDTO):
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
            description="Phone of the firm",
            example="Phone number",
            min_length=1,
            max_length=255,
        )
    ]
    email: Annotated[
        EmailStr | None,
        Field(
            alias="email",
            description="Email of the firm",
            example="Email",
            min_length=1,
            max_length=255,
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
    address: Annotated[
        AddressDTO,
        Field(
            alias="address",
            description="Address of the firm",
        )
    ]
