from uuid import UUID

from app.common.exceptions import NotFoundException

from ..models import Catalogo
from .base import AsyncMemoryRepository


class CatalogoRepository(AsyncMemoryRepository[Catalogo, UUID]):

    async def find_by_name(self, name: str) -> Catalogo:
        """
        Busca um alguma coisa pelo nome.
        """
        result = next((s for s in self.memory if s["name"] == name), None)
        if result:
            return result
        raise NotFoundException()


__all__ = ["CatalogoRepository"]
    