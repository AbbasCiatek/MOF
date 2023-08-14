from datetime import datetime
from typing import Annotated

from beanie import Link
from pydantic import Field

from mof.abstract.model import AbstractDocument
from mof.user.models.user_doc import UserDocument


class SessionDocument(AbstractDocument):
    user_id: Annotated[
        Link[UserDocument],
        Field(
            alias="userId",
            description="User ID",
        )
    ]
    expires_at: Annotated[
        datetime,
        Field(
            alias="expiresAt",
        )
    ]
    login_at: Annotated[
        datetime,
        Field(
            alias="loginAt",
            default_factory=datetime.utcnow,
        )
    ] = datetime.utcnow()
    logout_at: Annotated[
        datetime | None,
        Field(
            alias="logoutAt",
        )
    ] = None
    last_seen_at: Annotated[
        datetime,
        Field(
            alias="lastSeenAt",
        )
    ]
    device: Annotated[
        str | None,
        Field(
            alias="device",
            min_length=1,
            max_length=500,
        )
    ] = None
    revoked: Annotated[
        bool,
        Field(
            alias="revoked",
        )
    ] = False
    refresh_token: Annotated[
        str | None,
        Field(
            alias="refreshToken",
            min_length=1,
        )
    ] = None

    class Settings:
        name = "session"
        use_revision = True


SessionDocument.model_rebuild()
