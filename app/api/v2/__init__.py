from fastapi import APIRouter

from app.settings import api_settings

SELLER_V2_PREFIX = "/seller/v2"

router_seller = APIRouter(prefix=SELLER_V2_PREFIX)


def load_routes(router_seller: APIRouter):
    if api_settings.enable_seller_resources:
        from app.api.v2.routers.catalogo_seller_router import router as catalogo_router

        router_seller.include_router(catalogo_router)


load_routes(router_seller)