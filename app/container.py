from dependency_injector import containers, providers

from app.integrations.database.mongo_client import MongoClient

from app.repositories import CatalogoRepository, CatalogoRepositoryV1

from app.services import CatalogoService, HealthCheckService, CatalogoServiceV1

from app.settings.app import AppSettings

from app.integrations.auth.keycloak_adapter import KeycloakAdapter

from app.worker.description.creating_product_description import CreatingProductDescription

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # -----------------------
    # ** Integrações com o BD
    # Em uma aplicação normal teríamos apenas
    # um cliente de banco de dados

    mongo_client = providers.Singleton(MongoClient, config.app_db_url_mongo)
    
    keycloak_adapter = providers.Singleton(KeycloakAdapter, config.app_openid_wellknown)
    
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
    catalogo_service = providers.Singleton(CatalogoService, catalogo_repository)

    # -----------------------
    
    # ** Health Check Service
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    from app.settings.worker import WorkerSettings
    configapi = providers.Configuration()
    creating_product_description = providers.Singleton(
        CreatingProductDescription,
        ia_api_url=configapi.ia_api_url,
        ia_model=configapi.ia_model,
        )
