from mof.auth.router import router as auth_router
from mof.firm.router import router as firm_router
from mof.health.router import router as health_router
from mof.user.router import router as user_router


def get_routes(api):
    api.include_router(health_router)
    api.include_router(auth_router, prefix="/api/v1")
    api.include_router(user_router, prefix="/api/v1")
    api.include_router(firm_router, prefix="/api/v1")
