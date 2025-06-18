import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import asyncio
import pymongo

from app.api.api_application import create_app
from app.api.router import routes
from app.container import Container
from app.models import CatalogoModel
from app.repositories import CatalogoRepositoryV1
from app.services import HealthCheckService
from app.settings import api_settings
from app.services import CatalogoServiceV1
from app.services import CatalogoService

#v2

from motor.motor_asyncio import AsyncIOMotorClient
from app.repositories.catalogo_repository import CatalogoRepository


"""@pytest.fixture
def container() -> Generator[Container, None, None]:
    container = Container()
    container.config.from_pydantic(api_settings)
    container.catalogo_repository.override(FakeCatalogoRepository())
    container.catalogo_service.override(CatalogoServiceV1(container.catalogo_repository()))
    yield container
    container.unwire()"""

"""@pytest.fixture
def app(container: Container) -> Generator[FastAPI, None, None]:
    import app.api.common.routers.health_check_routers as health_check_routers
    import app.api.v1.routers.catalogo_seller_router as catalogo_seller_router_v1
    import app.api.v2.routers.catalogo_seller_router as catalogo_seller_router_v2
    from app.services import CatalogoServiceV1

    container.catalogo_service.override(CatalogoServiceV1(container.catalogo_repository()))

    container.wire(
        modules=[
            health_check_routers,
            catalogo_seller_router_v1,
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
        yield client_instance"""

@pytest.fixture
def health_check_service(container: Container) -> HealthCheckService:
    return container.health_check_service()


# -------------------------------- FIXTURE PARA V1 --------------------
@pytest.fixture
def test_catalogo_v1() -> list[CatalogoModel]:
    return [
        CatalogoModel(
            seller_id="magalu2",
            sku="ma2cel",
            name="celular",


        ),
        CatalogoModel(
            seller_id="magalu3",
            sku="ma3notebook",
            name="notebook",


        ),
    ]


@pytest.fixture
def container_v1(test_catalogo_v1) -> Container:
    container = Container()
    container.config.from_pydantic(api_settings)
    repo = container.catalogo_repository_v1()
    # Popula o singleton do container!
    async def populate_repo(repo, produtos):
        for produto in produtos:
            await repo.create(produto)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(populate_repo(repo, test_catalogo_v1))
    loop.close()
    # Não sobrescreva o provider, pois já é singleton!
    container.catalogo_service_v1.override(CatalogoServiceV1(repo))
    return container

@pytest.fixture
def app_v1(container_v1: Container) -> FastAPI:
    import app.api.v1.routers.catalogo_seller_router as catalogo_seller_router_v1
    container_v1.wire(modules=[catalogo_seller_router_v1])
    app_instance = create_app(api_settings, routes)
    app_instance.container = container_v1  # type: ignore[attr-defined]
    yield app_instance
    container_v1.unwire()

@pytest.fixture
def client_v1(app_v1: FastAPI) -> TestClient:
    with TestClient(app_v1) as client:
        yield client



# --------------------------- FIXTURE PARA V2 -------------------------

# --- FIXTURE DE MOCK PARA O REPOSITÓRIO DE CATÁLOGO ---


#Acessar o banco diretamente
@pytest.fixture
def mongo_clientv2():
    return AsyncIOMotorClient("mongodb://admin:admin@localhost:27018/test_db?authSource=admin")

"""@pytest.fixture
def repository(mongo_clientv2):
    return CatalogoRepository(mongo_clientv2)"""

@pytest.fixture(autouse=True)
def clean_catalogo_collection():
    client = pymongo.MongoClient("mongodb://admin:admin@localhost:27018/test_db?authSource=admin")
    db = client.get_default_database()
    db["catalogo"].delete_many({})
    yield
    db["catalogo"].delete_many({})
    client.close()

#testar as rotas http da api
@pytest.fixture
def container_v2(mongo_clientv2) -> Container:
    container = Container()
    container.config.from_pydantic(api_settings)
    repo = CatalogoRepository(mongo_clientv2)  # Agora mongo_clientv2 é a instância!
    container.catalogo_repository.override(repo)
    container.catalogo_service.override(CatalogoService(repo))
    return container

@pytest.fixture
def app_v2(container_v2: Container) -> FastAPI:
    import app.api.v2.routers.catalogo_seller_router as catalogo_seller_router_v2
    container_v2.wire(modules=[catalogo_seller_router_v2])
    app_instance = create_app(api_settings, routes)
    app_instance.container = container_v2  # type: ignore[attr-defined]
    yield app_instance
    container_v2.unwire()

@pytest.fixture
def client_v2(app_v2: FastAPI) -> TestClient:
    with TestClient(app_v2) as client:
        yield client

@pytest.fixture
def repository(mongo_clientv2):
    return CatalogoRepository(mongo_clientv2)


"""
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

    async def find_by_seller_id(self, seller_id: str):
        return [item for item in self._data if item.seller_id == seller_id]"""




"""@pytest.fixture
def test_catalogo():
    return [
        CatalogoModel(seller_id="magalu1", sku="ma1tv", name="tv50"),
        CatalogoModel(seller_id="magalu2", sku="ma2cel", name="celular"),
    ]"""

"""@pytest.fixture
def populate_catalogo(repository, test_catalogo):
    # Insere os produtos no banco Mongo antes do teste
    import asyncio
    async def _populate():
        for produto in test_catalogo:
            await repository.create(produto)
    asyncio.get_event_loop().run_until_complete(_populate())
    return test_catalogo
"""
