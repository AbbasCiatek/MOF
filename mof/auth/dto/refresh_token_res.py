from typing import Annotated

from pydantic import BaseModel, Field


class RefreshTokenResponseDTO(BaseModel):
    accessToken: Annotated[
        str,
        Field(
            alias="accessToken",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            description="Short-lived token used to authenticate the user",
        )
    ]
