from typing import Generator
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.api_application import create_app
from app.api.router import routes
from app.container import Container
from app.models import CatalogoModel
from app.repositories import CatalogoRepository
from app.services import HealthCheckService
from app.settings import api_settings

# --- FIXTURE DE MOCK PARA O REPOSITÓRIO DE CATÁLOGO ---
class FakeCatalogoRepository:
    def __init__(self):
        self._data = [
            CatalogoModel(seller_id="magalu1", sku="ma1tv", name="tv50"),
            CatalogoModel(seller_id="magalu2", sku="ma2cel", name="celular"),
        ]

    async def find_product(self, seller_id: str, sku: str):
        for item in self._data:
            if item.seller_id == seller_id and item.sku == sku:
                return item
        return None

    async def find(self, filters: dict, limit: int = 20, offset: int = 0, sort: dict | None = None):
        seller_id = filters.get("seller_id")
        if seller_id:
            return [item for item in self._data if item.seller_id == seller_id]
        return self._data

    async def create(self, entity):
        self._data.append(entity)
        return entity

    async def update_by_sellerid_sku(self, seller_id, sku, entity):
        for idx, item in enumerate(self._data):
            if item.seller_id == seller_id and item.sku == sku:
                self._data[idx] = entity
                return entity
        return None

    async def patch_by_sellerid_sku(self, seller_id, sku, patch_entity):
        for idx, item in enumerate(self._data):
            if item.seller_id == seller_id and item.sku == sku:
                for k, v in patch_entity.items():
                    setattr(self._data[idx], k, v)
                return self._data[idx]
        return None

    async def delete_by_sellerid_sku(self, seller_id, sku):
        for idx, item in enumerate(self._data):
            if item.seller_id == seller_id and item.sku == sku:
                del self._data[idx]
                return True
        return False

@pytest.fixture
def test_catalogo():
    return [
        CatalogoModel(seller_id="magalu1", sku="ma1tv", name="tv50"),
        CatalogoModel(seller_id="magalu2", sku="ma2cel", name="celular"),
    ]

@pytest.fixture
def container() -> Generator[Container, None, None]:
    container = Container()
    container.config.from_pydantic(api_settings)
    container.catalogo_repository.override(FakeCatalogoRepository())
    yield container
    container.unwire()

@pytest.fixture
def app(container: Container) -> Generator[FastAPI, None, None]:
    import app.api.common.routers.health_check_routers as health_check_routers
    import app.api.v2.routers.catalogo_seller_router as catalogo_seller_router_v2

    container.wire(
        modules=[
            health_check_routers,
            catalogo_seller_router_v2,
        ]
    )
    app_instance = create_app(api_settings, routes)
    app_instance.container = container  # type: ignore[attr-defined]
    yield app_instance
    container.unwire()

@pytest.fixture
def client(app: FastAPI) -> Generator[TestClient, None, None]:
    with TestClient(app) as client_instance:
        yield client_instance

@pytest.fixture
def health_check_service(container: Container) -> HealthCheckService:
    return container.health_check_service()