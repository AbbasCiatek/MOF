import pymongo
from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from pymongo.errors import DuplicateKeyError

from mof.abstract.constants import Order
from mof.exceptions import APIException
from mof.user.dto.create_user_dto import CreateUserDTO
from mof.user.dto.update_user_dto import UpdateUserDTO
from mof.user.dto.user_filters import UserFilters
from mof.user.dto.user_page_options import UserPageOptions, UserSortingFields
from mof.user.errors import user_errors, user_unique_err_handle
from mof.user.models.user_doc import UserDocument


class UserService:
    async def create_user(self, dto: CreateUserDTO) -> UserDocument:
        try:
            user = UserDocument(**dto.model_dump())
            await user.insert()
            return user
        except DuplicateKeyError as e:
            user_unique_err_handle(e)
            raise APIException(user_errors.not_found)

    async def get_users(self, filters: UserFilters, page_options: UserPageOptions) -> Page[UserDocument]:
        user_query = UserDocument.find_many(filters.model_dump(exclude_none=True))

        if page_options.search:
            user_query = user_query.find_many({"$text": {"$search": page_options.search}})

        sort = page_options.sort if page_options.sort else UserSortingFields.created_at
        order = pymongo.ASCENDING if page_options.order == Order.ASC else pymongo.DESCENDING
        user_query = user_query.sort((sort, order))

        users = await paginate(user_query)
        return users

    async def get_user(self, id: PydanticObjectId) -> UserDocument | None:

        user = await UserDocument.get(id)
        return user

    async def update_user(
            self,
            id: PydanticObjectId,
            dto: UpdateUserDTO,
    ) -> UserDocument:
        user = await UserDocument.get(id)
        if not user:
            raise APIException(user_errors.not_found)

        try:
            update_data = dto.model_dump(exclude_none=True, by_alias=True)
            user = await user.update(Set(update_data))
        except DuplicateKeyError as e:
            user_unique_err_handle(e)

        return user

    async def delete_user(self, id: PydanticObjectId) -> None:
        user = await UserDocument.get(id)
        if not user:
            raise APIException(user_errors.not_found)

        await user.delete()
        return

    async def find_by_email(self, email: str) -> UserDocument | None:
        user = await UserDocument.find_many({UserDocument.email: email}).first_or_none()
        return user


user_service = UserService()
