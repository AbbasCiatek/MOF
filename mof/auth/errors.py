from typing import Annotated

from pydantic import BaseModel, Field

from mof.exceptions import ErrorType, api_errors, load_errors


class AuthErrors(BaseModel):
    expired_token: Annotated[
        ErrorType,
        Field(alias="expiredToken")
    ]
    invalid_token: Annotated[
        ErrorType,
        Field(alias="invalidToken")
    ]
    missing_token: Annotated[
        ErrorType,
        Field(alias="missingToken")
    ]
    invalid_credentials: Annotated[
        ErrorType,
        Field(alias="invalidCredentials")
    ]
    deactivated: Annotated[
        ErrorType,
        Field(alias="deactivated")
    ]
    no_session: Annotated[
        ErrorType,
        Field(alias="noSession")
    ]
    session_revoked: Annotated[
        ErrorType,
        Field(alias="sessionRevoked")
    ]
    unauthorized: Annotated[
        ErrorType,
        Field(alias="unauthorized")
    ]
    forbidden: Annotated[
        ErrorType,
        Field(alias="forbidden")
    ]


auth_errors = AuthErrors.model_validate(load_errors('auth'))
