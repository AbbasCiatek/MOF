from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends
from fastapi_pagination import Page

from mof.exceptions import APIException, ErrorType
from mof.user.dto.create_user_dto import CreateUserDTO
from mof.user.dto.update_user_dto import UpdateUserDTO
from mof.user.dto.user_dto import UserDTO
from mof.user.dto.user_filters import UserFilters
from mof.user.dto.user_page_options import UserPageOptions
from mof.user.errors import user_errors
from mof.user.models.user_doc import UserDocument
from mof.user.services.user_service import UserService

router = APIRouter(
    prefix="/users"
)
user_service = UserService()


@router.post(
    "/",
    response_model=UserDTO,
    tags=["user"],
    responses={
        400: {
            "model": ErrorType,
            "description": "Invalid data",
            "content": {
                "application/json": {
                    "example": [
                        user_errors.invalid_password.model_dump(exclude_none=False),
                    ]

                },
            }
        },
        409: {
            "model": ErrorType,
            "description": "Email already exists",
            "content": {
                "application/json": {
                    "example": [
                        user_errors.email_exists.model_dump(exclude_none=False),
                        user_errors.phone_exists.model_dump(exclude_none=False),
                    ]

                }
            }
        }
    }
)
async def create_user(
        user_create: CreateUserDTO = Body(...),
) -> UserDocument:
    user = await user_service.create_user(user_create)
    return user


@router.get("/", response_model=Page[UserDTO], tags=["user"])
async def list_users(
        filters: UserFilters = Depends(),
        page_options: UserPageOptions = Depends(),
) -> Page[UserDocument]:
    users = await user_service.get_users(filters, page_options)
    return users


@router.get(
    path="/{id}",
    response_model=UserDTO,
    tags=["user"],
    responses={
        404: {
            "model": ErrorType,
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": user_errors.not_found.model_dump(exclude_none=False)
                }
            }
        }
    }
)
async def get_user(
        id: PydanticObjectId,
) -> UserDocument:
    user = await user_service.get_user(id)
    if not user:
        raise APIException(user_errors.not_found)
    return user


@router.put(
    path="/users/{id}",
    response_model=UserDTO,
    tags=["user"],
    responses={
        404: {
            "model": ErrorType,
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": user_errors.not_found.model_dump(exclude_none=False)
                }
            }
        }
    }
)
async def update_user(
        id: PydanticObjectId,
        user_update: UpdateUserDTO = Body(...),
) -> UserDocument:
    return await user_service.update_user(id, user_update)


@router.delete(
    path="/users/{id}",
    response_model=None,
    tags=["user"],
    responses={
        404: {
            "model": ErrorType,
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": user_errors.not_found.model_dump(exclude_none=False)
                }
            }
        }
    }
)
async def delete_user(
        id: PydanticObjectId,
) -> None:
    return await user_service.delete_user(id)
