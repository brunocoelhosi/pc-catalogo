from dependency_injector import containers, providers

from app.repositories import CatalogoRepository
from app.services import HealthCheckService, CatalogoService
from app.settings import AppSettings


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    settings = providers.Singleton(AppSettings)

    # Repositórios
    catalogo_repository = providers.Singleton(CatalogoRepository)

    # Serviços
    health_check_service = providers.Singleton(
        HealthCheckService, checkers=config.health_check_checkers, settings=settings
    )

    catalogo_service = providers.Singleton(CatalogoService, repository=catalogo_repository)
