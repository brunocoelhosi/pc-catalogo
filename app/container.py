from dependency_injector import containers, providers

from app.integrations.database.mongo_client import MongoClient

from app.repositories import CatalogoRepository, CatalogoRepositoryV1

from app.services import CatalogoService, HealthCheckService, CatalogoServiceV1

from app.settings.app import AppSettings



class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # -----------------------
    # ** Integrações com o BD
    # Em uma aplicação normal teríamos apenas
    # um cliente de banco de dados

    mongo_client = providers.Singleton(MongoClient, config.app_db_url_mongo)

    # -----------------------
    # ** Repositórios
    #

    #v2
    catalogo_repository = providers.Singleton(CatalogoRepository, mongo_client)
    
    #v1
    catalogo_repository.override(CatalogoRepositoryV1())

    # -----------------------
    # ** Servicos
    #

    #v2
    catalogo_service = providers.Singleton(CatalogoService, catalogo_repository)

    #v1
    catalogo_service.override(CatalogoServiceV1(catalogo_repository()))


    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

