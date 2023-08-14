from enum import Enum
from typing import Annotated

from fastapi import Query

from mof.abstract.page_options import AbstractPageOptions


class UserSortingFields(str, Enum):
    first_name = "firstName"
    last_name = "lastName"
    email = "email"
    role = "role"
    phone = "phone"
    created_at = "createdAt"


class UserPageOptions(AbstractPageOptions):
    sort: Annotated[
        UserSortingFields,
        Query(
            alias="sort",
            examples=["email"],
            description="User sorting field, should be one of the provided values.",
            min_length=1,
            max_length=50,
        )
    ] = UserSortingFields.created_at
