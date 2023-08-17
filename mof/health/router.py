from datetime import datetime

from fastapi import APIRouter

from mof import __version__
from mof.logger import logger
from mof.types import HealthcheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthcheckResponse, tags=["health"])
def healthcheck() -> HealthcheckResponse:
    message = "We're on the air."
    time = datetime.now()
    logger.info(msg=message, extra={"version": __version__, "time": time})
    return HealthcheckResponse(
        message=message, version=__version__, time=datetime.now()
    )

@router.get("/health/ready", response_model=HealthcheckResponse, tags=["health"])
def ready() -> HealthcheckResponse:
    message = "We're ready."
    time = datetime.now()
    logger.info(msg=message, extra={"version": __version__, "time": time})
    return HealthcheckResponse(
        message=message, version=__version__, time=datetime.now()
    )

