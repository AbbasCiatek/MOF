from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

from mof.abstract.constants import Order


class AbstractPageOptions(BaseModel):
    order: Annotated[
        Order,
        Query(
            alias="order",
            examples=["ASC"],
            description="Sort order, should be either DESC or ASC.",
        )
    ] = Order.DESC
    search: Annotated[
        str | None,
        Query(
            alias="search",
            examples=["John"],
            description="Search string, should be a valid string. Min length is 1, max length is 100.",
            min_length=1,
            max_length=100
        )
    ] = None
