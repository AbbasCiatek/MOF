import pymongo
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import paginate
from pymongo.errors import DuplicateKeyError

from mof.abstract.constants import Order
from mof.exceptions import APIException
from mof.firm.dto.create_firm_dto import CreateFirmDTO
from mof.firm.dto.firm_filters import FirmFilters
from mof.firm.dto.firm_page_options import FirmPageOptions, FirmSortingFields
from mof.firm.dto.update_firm_dto import UpdateFirmDTO
from mof.firm.errors import firm_errors
from mof.firm.errors import firm_unique_err_handle
from mof.firm.models.firm_doc import FirmDocument


class FirmService:
    async def create_firm(self, firm: CreateFirmDTO) -> FirmDocument:
        try:
            firm = FirmDocument(**firm.model_dump())
            await firm.insert()
            return firm
        except DuplicateKeyError as e:
            firm_unique_err_handle(e)

    async def get_firms(self, filters: FirmFilters, page_options: FirmPageOptions) -> Page[FirmDocument]:
        firm_query = FirmDocument.find_many(filters.model_dump(exclude_none=True))

        if page_options.search:
            firm_query = firm_query.find_many({"$text": {"$search": page_options.search}})

        sort = page_options.sort if page_options.sort else FirmSortingFields.created_at
        order = pymongo.ASCENDING if page_options.order == Order.ASC else pymongo.DESCENDING
        firm_query = firm_query.sort((sort, order))

        firms = await paginate(firm_query)
        return firms

    async def get_firm(self, firm_id: PydanticObjectId):
        firm = await FirmDocument.get(firm_id)
        if not firm:
            raise APIException(firm_errors.not_found)

        return firm

    async def update_firm(self, firm_id: PydanticObjectId, dto: UpdateFirmDTO):
        firm = await FirmDocument.get(firm_id)
        if not firm:
            raise APIException(firm_errors.not_found)

        try:
            return await firm.update(dto.model_dump(exclude_none=True))
        except DuplicateKeyError as e:
            firm_unique_err_handle(e)

    async def delete_firm(self, firm_id: PydanticObjectId):
        firm = await FirmDocument.get(firm_id)
        if not firm:
            raise APIException(firm_errors.not_found)

        await firm.delete()
        return firm


firm_service = FirmService()
