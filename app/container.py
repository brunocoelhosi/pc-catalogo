from dependency_injector import containers, providers
from app.integrations.database.mongo_client import MongoClient
from app.repositories import CatalogoRepository, CatalogoRepositoryV1
from app.services import CatalogoService, HealthCheckService, CatalogoServiceV1
from app.settings.app import AppSettings
from app.integrations.auth.keycloak_adapter import KeycloakAdapter
from app.worker.description.creating_product_description import CreatingProductDescription
from app.integrations.cache.redis_asyncio_adapter import RedisAsyncioAdapter

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # -----------------------
    # ** Client MongoDB 
    mongo_client = providers.Singleton(MongoClient, config.app_db_url_mongo)
    # ** Client Keycloak Adapter
    keycloak_adapter = providers.Singleton(KeycloakAdapter, config.app_openid_wellknown)
    
    #------------------------
    # ** Redis
    redis_adapter = providers.Singleton(RedisAsyncioAdapter, config.app_redis_url)
    
    
    # V1 - Memory
    # ** Repositório
    catalogo_repository_v1 = providers.Singleton(CatalogoRepositoryV1)
    # ** Servico
    catalogo_service_v1 = providers.Singleton(CatalogoServiceV1, catalogo_repository_v1)

    # -----------------------

    # V2 - MongoDB
    # ** Repositório
    catalogo_repository = providers.Singleton(CatalogoRepository, mongo_client)
    # ** Servico
    catalogo_service = providers.Singleton(CatalogoService, catalogo_repository, redis_adapter=redis_adapter)

    # -----------------------
    
    # ** Health Check Service
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )
    
    #------------------------
    # ** Worker IA
    creating_product_description = providers.Singleton(
        CreatingProductDescription,
        ia_api_url=config.ia_api_url,
        ia_model=config.ia_model,
        )

