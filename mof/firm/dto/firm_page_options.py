from enum import Enum
from typing import Annotated

from fastapi import Query

from mof.abstract.page_options import AbstractPageOptions


class FirmSortingFields(str, Enum):
    name = "name"
    phone = "phone"
    email = "email"
    created_at = "createdAt"
    updated_at = "updatedAt"


class FirmPageOptions(AbstractPageOptions):
    sort: Annotated[
        FirmSortingFields,
        Query(
            alias="sort",
            description="Sort by field",
            example="name",
            title="Sort by field, should be one of the provided values",
            min_length=1,
            max_length=50,
        )
    ] = FirmSortingFields.name
