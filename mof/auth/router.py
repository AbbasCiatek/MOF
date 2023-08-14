from fastapi import APIRouter, Depends, Body

from mof.auth.dto.login_dto import LoginDTO
from mof.auth.dto.login_response import LoginResponseDTO
from mof.auth.dto.refresh_token_res import RefreshTokenResponseDTO
from mof.auth.services.auth_service import auth_service
from mof.auth.errors import auth_errors
from mof.exceptions import ErrorType
from mof.user.dto.user_dto import UserDTO
from mof.user.errors import user_errors

router = APIRouter()


@router.post(
    path="/login",
    response_model=LoginResponseDTO,
    tags=["auth"],
    responses={
        400: {
            "model": ErrorType,
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": auth_errors.invalid_credentials.model_dump()
                }
            }
        },
        404: {
            "model": ErrorType,
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": user_errors.not_found.model_dump()
                }
            }
        },
        403: {
            "model": ErrorType,
            "description": "User deactivated",
            "content": {
                "application/json": {
                    "example": auth_errors.deactivated.model_dump()
                }
            }
        },
    }
)
async def login(dto: LoginDTO = Body(...)) -> LoginResponseDTO:
    return await auth_service.authenticate_user(dto=dto)


@router.post(
    path="/refresh",
    response_model=RefreshTokenResponseDTO,
    tags=["auth"], responses={
        401: {
            "model": ErrorType,
            "content": {
                "application/json": {
                    "example": [
                        auth_errors.missing_token.model_dump(),
                        auth_errors.invalid_token.model_dump(),
                        auth_errors.expired_token.model_dump()
                    ]
                },
            },
        },
        403: {
            "model": ErrorType,
            "description": "User deactivated",
            "content": {
                "application/json": {
                    "example": [
                        auth_errors.deactivated.model_dump(),
                        auth_errors.session_revoked.model_dump(),
                        auth_errors.no_session.model_dump(),
                    ]
                }
            },
        },
        404: {
            "model": ErrorType,
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": user_errors.not_found.model_dump()
                }
            }
        }
    })
async def refresh_token(
        token: str = Depends(auth_service.refresh_token_schema),
) -> RefreshTokenResponseDTO:
    return await auth_service.refresh_token(token=token)


@router.get("/me", response_model=UserDTO, tags=["auth"], responses={
    401: {
        "model": ErrorType,
        "description": "Invalid credentials",
        "content": {
            "application/json": {
                "example": auth_errors.unauthorized.model_dump()
            }
        }
    },
    403: {
        "model": ErrorType,
        "description": "User deactivated",
        "content": {
            "application/json": {
                "example": auth_errors.deactivated.model_dump(),
            }
        },
    },
    404: {
        "model": ErrorType,
        "description": "User not found",
        "content": {
            "application/json": {
                "example": user_errors.not_found.model_dump()
            }
        }
    },
})
def current_user(payload=Depends(auth_service.current_user)) -> UserDTO:
    user = UserDTO.model_validate(payload)
    return user


@router.post("/logout", response_model=None, tags=["auth"])
async def logout(token: str = Depends(auth_service.refresh_token_schema)) -> None:
    return await auth_service.logout(token=token)
