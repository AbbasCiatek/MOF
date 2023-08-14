from datetime import datetime
from typing import Annotated

from beanie import Document, Insert, Save, Update, Replace, before_event, PydanticObjectId
from pydantic import Field


class AbstractDocument(Document):
    id: Annotated[
        PydanticObjectId,
        Field(
            alias="_id",
            default_factory=PydanticObjectId,
        )
    ]
    created_at: Annotated[
        datetime,
        Field(
            alias="createdAt",
            default_factory=datetime.utcnow
        )
    ]
    updated_at: Annotated[
        datetime,
        Field(
            alias="updatedAt",
            default_factory=datetime.utcnow
        )
    ]

    @before_event( Save, Update, Replace)
    def update_date(self):
        self.updated_at = datetime.utcnow()
