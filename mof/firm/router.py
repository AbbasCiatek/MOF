from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends
from fastapi_pagination import Page

from mof.exceptions import ErrorType
from mof.firm.dto.firm_dto import FirmDTO
from mof.firm.dto.firm_filters import FirmFilters
from mof.firm.dto.firm_page_options import FirmPageOptions
from mof.firm.errors import firm_errors
from mof.firm.models.firm_doc import FirmDocument
from mof.firm.services.firm_service import firm_service

router = APIRouter(
    prefix="/firms",
)


@router.post("/", response_model=FirmDTO, tags=["firm"], responses={
    409: {
        "model": ErrorType,
        "description": "Firm already exists",
        "content": {
            "application/json": {
                "example": [
                    firm_errors.name_exists.model_dump(exclude_none=False),
                    firm_errors.email_exists.model_dump(exclude_none=False),
                    firm_errors.phone_exists.model_dump(exclude_none=False),
                    firm_errors.mof_exists.model_dump(exclude_none=False),
                ]
            }
        }
    }
})
async def create_firm(
        firm_create: FirmDTO = Body(..., embed=True),
) -> FirmDocument:
    firm = await firm_service.create_firm(firm_create)
    return firm


@router.get("/", response_model=Page[FirmDTO], tags=["firm"])
async def get_firms(
        filters: FirmFilters = Depends(),
        page_options: FirmPageOptions = Depends(),
) -> list[FirmDocument]:
    firms = await firm_service.get_firms(filters, page_options)
    return firms


@router.get(
    path="/{id}",
    response_model=FirmDTO,
    tags=["firm"],
    responses={
        404: {
            "model": ErrorType,
            "description": "Firm not found",
            "content": {
                "application/json": {
                    "example": [
                        firm_errors.not_found.model_dump(exclude_none=False),
                    ]
                }
            }
        }
    }
)
async def get_firm_by_id(
        id: PydanticObjectId,
) -> FirmDocument:
    firm = await firm_service.get_firm_by_id(id)
    return firm


@router.put(
    path="/{id}",
    response_model=FirmDTO,
    tags=["firm"],
    responses={
        404: {
            "model": ErrorType,
            "description": "Firm not found",
            "content": {
                "application/json": {
                    "example": [
                        firm_errors.not_found.model_dump(exclude_none=False),
                    ]
                }
            }
        },
        409: {
            "model": ErrorType,
            "description": "Firm already exists",
            "content": {
                "application/json": {
                    "example": [
                        firm_errors.name_exists.model_dump(exclude_none=False),
                        firm_errors.email_exists.model_dump(exclude_none=False),
                        firm_errors.phone_exists.model_dump(exclude_none=False),
                        firm_errors.mof_exists.model_dump(exclude_none=False),
                    ]
                }
            }
        }
    }
)
async def update_firm(
        id: PydanticObjectId,
        firm_update: FirmDTO = Body(..., embed=True),
) -> FirmDocument:
    firm = await firm_service.update_firm(id, firm_update)
    return firm


@router.delete(
    path="/{id}",
    response_model=None,
    tags=["firm"],
    responses={
        404: {
            "model": ErrorType,
            "description": "Firm not found",
            "content": {
                "application/json": {
                    "example": [
                        firm_errors.not_found.model_dump(exclude_none=False),
                    ]
                }
            }
        }
    }
)
async def delete_firm(
        id: PydanticObjectId,
) -> None:
    await firm_service.delete_firm(id)
