from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class LoginDTO(BaseModel):
    email: Annotated[
        EmailStr,
        Field(
            alias="email",
            example="smith@ciatek.net",
            description="Email address of the user",
        )
    ]
    password: Annotated[
        str,
        Field(
            alias="password",
            example="password",
            description="Password of the user",
        )
    ]
