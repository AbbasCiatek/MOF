from enum import Enum
from typing import Annotated

import pymongo
from beanie import before_event, Insert, Update, Replace, Link
from pydantic import EmailStr, Field, StrictStr
from pydantic_extra_types.phone_numbers import PhoneNumber
from pymongo import IndexModel

from mof.abstract.model import AbstractDocument
from mof.auth.services.crypto_service import crypto_service
from mof.firm.models.firm_doc import FirmDocument
from mof.user.constants import RoleEnum


class UserIndexes(str, Enum):
    unique_email = "user_unique_email"
    unique_phone = "user_unique_phone"
    user_search = "user_search"


class UserDocument(AbstractDocument):
    email: Annotated[
        EmailStr,
        Field(
            alias="email",
            min_length=1,
            max_length=480,
        )
    ]
    first_name: Annotated[
        StrictStr,
        Field(
            alias="firstName",
            min_length=1,
            max_length=50,
            pattern="^[a-zA-Z]*$",
        )
    ]
    last_name: Annotated[
        StrictStr,
        Field(
            alias="lastName",
            min_length=1,
            max_length=50,
            pattern="^[a-zA-Z]*$",
        )
    ]
    password: Annotated[
        StrictStr,
        Field(
            alias="password",
        )
    ]
    role: Annotated[
        RoleEnum,
        Field(
            alias="role",
            min_length=1,
            max_length=50,
        )
    ]
    deactivated: Annotated[
        bool,
        Field(
            alias="deactivated",
        )
    ] = False
    phone: Annotated[
        PhoneNumber,
        Field(
            alias="phone",
            min_length=1,
            max_length=100,
        )
    ]
    firms: Annotated[
        list[Link[FirmDocument]],
        Field(
            alias="firms",
        )
    ] = []

    @before_event(Insert, Update, Replace)
    def hash_password(self):
        if self.id is not None and self.password is None:
            doc = self.get_document_by_id(self.id)
            doc_pass = doc.password if doc else None

            if doc and crypto_service.verify_password(self.password, doc_pass):
                return

        if self.password is not None:
            self.password = crypto_service.hash_password(self.password)

    class Settings:
        name = "user"
        use_revision = True
        indexes = [
            IndexModel([("email", pymongo.ASCENDING)], unique=True, name=UserIndexes.unique_email),
            IndexModel([("phone", pymongo.ASCENDING)], unique=True, name=UserIndexes.unique_phone),
            IndexModel([
                ("firstName", pymongo.TEXT),
                ("email", pymongo.TEXT),
                ("lastName", pymongo.TEXT)
            ], name="user_search")
        ]


UserDocument.model_rebuild()
