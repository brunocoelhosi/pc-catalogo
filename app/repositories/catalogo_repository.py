from typing import TYPE_CHECKING
from uuid import UUID

from ..models import CatalogoModel
from .base import MongoCatalogoRepository

from .base import AsyncMemoryRepository

if TYPE_CHECKING:
    from app.integrations.database.mongo_client import MongoClient


class CatalogoRepository(MongoCatalogoRepository[CatalogoModel, UUID]):

    COLLECTION_NAME = "catalogo"

    def __init__(self, client: "MongoClient"):
        super().__init__(client, collection_name=self.COLLECTION_NAME, model_class=CatalogoModel)


class CatalogoRepositoryV1(AsyncMemoryRepository[CatalogoModel, UUID]):

    """ """

__all__ = ["CatalogoRepository", "CatalogoRepositoryV1"]





