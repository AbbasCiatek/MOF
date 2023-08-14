from datetime import datetime
from typing import Annotated

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class AbstractDTO(BaseModel):
    id: Annotated[
        PydanticObjectId,
        Field(
            alias="id",
            example="00000000-0000-0000-0000-000000000000",
            description="Unique identifier in Mongo ObjectId format."
        )]
    created_at: Annotated[
        datetime,
        Field(
            alias="createdAt",
            example="2021-01-01T00:00:00.000Z",
            description="Creation date in ISO format."
        )]
    updated_at: Annotated[
        datetime,
        Field(
            alias="updatedAt",
            example="2021-01-01T00:00:00.000Z",
            description="Update date in ISO format."
        )
    ]

    class Config:
        populate_by_name = True
