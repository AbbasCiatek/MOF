from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Query
from pydantic import BaseModel


class AbstractFilters(BaseModel):
    id: Annotated[
        PydanticObjectId | None,
        Query(
            alias="id",
            examples=["00000000-0000-0000-0000-000000000000"],
            description="Unique identifier in UUID4 format.",
        )
    ] = None
    created_at: Annotated[
        datetime | None,
        Query(
            alias="createdAt",
            examples=["2021-01-01T00:00:00.000Z"],
            description="Creation date in ISO format.",
        )
    ] = None
    updated_at: Annotated[
        datetime | None,
        Query(
            alias="updatedAt",
            examples=["2021-01-01T00:00:00.000Z"],
            description="Update date in ISO format.",
        )
    ] = None
