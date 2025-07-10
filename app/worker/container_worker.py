from dependency_injector import containers, providers

from app.integrations.database.mongo_client import MongoClient
from app.repositories import CatalogoRepository

from app.settings.worker import WorkerSettings
from app.services.catalogo.catalogo_service import CatalogoService
from app.models.catalogo_model import CatalogoModel

import app.services.catalogo.catalogo_service as catalogo_service_module

from app.container import Container
import app.services.catalogo.catalogo_service as catalogo_service_module



from app.worker.description.creating_product_description import CreatingProductDescription

class WorkerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    settings = providers.Singleton(WorkerSettings)

    # Integrações
    mongo_client = providers.Singleton(MongoClient, config.app_db_url)

    # Repositórios
    catalogo_repository = providers.Singleton(CatalogoRepository, mongo_client)

    # Serviços
    # (adicione outros serviços aqui)

    # Tarefas
    creating_product_description = providers.Singleton(
        CreatingProductDescription, ia_api_url=config.ia_api_url, ia_model=config.ia_model
    )

    container = Container()
    container.wire(modules=[catalogo_service_module])