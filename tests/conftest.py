import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import asyncio
import pymongo

from app.api.api_application import create_app
from app.api.router import routes

from app.models import CatalogoModel
from app.repositories import CatalogoRepositoryV1
from app.services import HealthCheckService
from app.settings import api_settings
from app.services import CatalogoServiceV1
from app.services import CatalogoService
from app.container import Container
#v2

from motor.motor_asyncio import AsyncIOMotorClient
from app.repositories.catalogo_repository import CatalogoRepository

from pytest import fixture
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator


from app.api.common.auth_handler import do_auth, get_current_user, UserAuthInfo
from app.models.base import UserModel

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
from unittest.mock import AsyncMock

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

"""#testar as rotas http da api
@pytest.fixture
def container_v2(mongo_clientv2) -> Container:
    container = Container()
    container.config.from_pydantic(api_settings)
    repo = CatalogoRepository(mongo_clientv2)  # Agora mongo_clientv2 é a instância!
    container.catalogo_repository.override(repo)
    container.catalogo_service.override(CatalogoService(repo))
    return container
"""
@pytest.fixture
def container_v2(mongo_clientv2) -> Container:
    container = Container()
    container.config.from_pydantic(api_settings)
    repo = CatalogoRepository(mongo_clientv2)
    container.catalogo_repository.override(repo)
    container.catalogo_service.override(CatalogoService(repo))

    # Mock do keycloak_adapter
    fake_adapter = AsyncMock()
    fake_adapter.validate_token.return_value = {
        "sub": "fake-user-id",
        "iss": "fake-issuer",
        "sellers": "magalu11"
    }
    container.keycloak_adapter.override(fake_adapter)
    return container
"""@pytest.fixture
def app_v2(container_v2: Container) -> FastAPI:
    import app.api.v2.routers.catalogo_seller_router as catalogo_seller_router_v2
    container_v2.wire(modules=[catalogo_seller_router_v2])
    app_instance = create_app(api_settings, routes)
    app_instance.container = container_v2  # type: ignore[attr-defined]
    yield app_instance
    container_v2.unwire()"""





@pytest.fixture
def repository(mongo_clientv2):
    return CatalogoRepository(mongo_clientv2)



@pytest.fixture(autouse=True)
def mock_do_auth(monkeypatch):
    async def fake_do_auth(request=None, *args, **kwargs):
        print("MOCK DO_AUTH CHAMADO")
        fake_user = UserModel(name="fake-user", server="fake-server")
        fake_user_info = UserAuthInfo(user=fake_user, trace_id=None, sellers=["magalu11", "magalu10", "sellerapi1", "magalu1", "magalu2"])
        if request is not None and hasattr(request, "state"):
            request.state.user = fake_user_info
        return fake_user_info

    # Patch global
    monkeypatch.setattr("app.api.common.auth_handler.do_auth", fake_do_auth)
    monkeypatch.setattr("app.api.common.auth_handler.get_current_user", fake_do_auth)

    # Patch local no router v2
    import app.api.v2.routers.catalogo_seller_router as router_v2
    monkeypatch.setattr(router_v2, "do_auth", fake_do_auth)
    monkeypatch.setattr(router_v2, "get_current_user", fake_do_auth)

    """@pytest.fixture(autouse=True)
    def mock_do_auth(monkeypatch):

        async def fake_do_auth(request=None, *args, **kwargs):
            print("MOCK DO_AUTH CHAMADO")
            fake_user = UserModel(name="fake-user", server="fake-server")
            fake_user_info = UserAuthInfo(user=fake_user, trace_id=None, sellers=["magalu11", "magalu10", "sellerapi1", "magalu1", "magalu2"])
            # Se o request for passado, define o atributo state.user (para get_current_user)
            if request is not None and hasattr(request, "state"):
                request.state.user = fake_user_info
            return fake_user_info
    """
    # Mocka do_auth (usado como Depends em routers)
    monkeypatch.setattr("app.api.common.auth_handler.do_auth", fake_do_auth)
    # Mocka get_current_user (usado como Depends em endpoints)
    monkeypatch.setattr("app.api.common.auth_handler.get_current_user", fake_do_auth)


@pytest.fixture
def app_v2(mock_do_auth, container_v2: Container) -> FastAPI:
    import app.api.v2.routers.catalogo_seller_router as catalogo_seller_router_v2
    import app.api.common.auth_handler as auth_handler
    container_v2.wire(modules=[catalogo_seller_router_v2, auth_handler])
    app_instance = create_app(api_settings, routes)
    app_instance.container = container_v2  # type: ignore[attr-defined]
    yield app_instance
    container_v2.unwire()

@pytest.fixture
async def async_client(app_v2) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app_v2)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def client_v2(app_v2: FastAPI) -> TestClient:
    with TestClient(app_v2) as client:
        yield client