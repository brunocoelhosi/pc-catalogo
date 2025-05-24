from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Catalogo
from .base import AsyncMemoryRepository


class CatalogoRepository(AsyncMemoryRepository[Catalogo, UUID]):

     """ """

__all__ = ["CatalogoRepository"]
    