from typing import Annotated

from pydantic import BaseModel, Field, StrictStr, EmailStr


class UpdateAddressDTO(BaseModel):
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
        StrictStr | None,
        Field(
            alias="building",
            description="Building of the firm",
            example="Building name",
            min_length=1,
            max_length=255,
        )
    ] = None
    street: Annotated[
        StrictStr | None,
        Field(
            alias="street",
            description="Street of the firm",
            example="Street name",
            min_length=1,
            max_length=255,
        )
    ] = None
    postal_code: Annotated[
        StrictStr | None,
        Field(
            alias="postalCode",
            description="Postal code of the firm",
            example="Postal code",
            min_length=1,
            max_length=255,
        )
    ] = None
    city: Annotated[
        StrictStr | None,
        Field(
            alias="city",
            description="City of the firm",
            example="City name",
            min_length=1,
            max_length=255,
        )
    ] = None
    sub_region: Annotated[
        StrictStr | None,
        Field(
            alias="subRegion",
            description="Sub region of the firm",
            example="Sub region name",
            min_length=1,
            max_length=255,
        )
    ] = None
    region: Annotated[
        StrictStr | None,
        Field(
            alias="region",
            description="Region of the firm",
            example="Region name",
            min_length=1,
            max_length=255,
        )
    ] = None
    country_of_origin: Annotated[
        StrictStr | None,
        Field(
            alias="countryOfOrigin",
            description="Country of the firm",
            example="Country name",
            min_length=1,
            max_length=255,
        )
    ] = None


class UpdateFirmDTO(BaseModel):
    name: Annotated[
        StrictStr | None,
        Field(
            alias="name",
            description="Name of the firm",
            example="Firm name",
            min_length=1,
            max_length=255,
        )
    ] = None
    phone: Annotated[
        StrictStr | None,
        Field(
            alias="phone",
            description="Phone of the firm",
            example="+380123456789",
            min_length=1,
            max_length=255,

        )
    ] = None
    email: Annotated[
        EmailStr | None,
        Field(
            alias="email",
            description="Email of the firm",
            example="someemail@somedomain.someextension",
            min_length=1,
            max_length=255,
        )
    ] = None
    mof: Annotated[
        StrictStr | None,
        Field(
            alias="mof",
            description="Mof of the firm",
            example="12345678",
            min_length=1,
            max_length=255,
        )
    ] = None
