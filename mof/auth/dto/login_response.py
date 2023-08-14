from typing import Annotated

from pydantic import BaseModel, Field

from mof.user.dto.user_dto import UserDTO


class LoginResponseDTO(BaseModel):
    access_token: Annotated[
        str,
        Field(
            alias="accessToken",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            description="Short-lived token used to authenticate the user",
        )
    ]
    refresh_token: Annotated[
        str,
        Field(
            alias="refreshToken",
            example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            description="Long-lived token used to refresh the access token",
        )
    ]
    user: UserDTO


