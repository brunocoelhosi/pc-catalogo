from ...models import Catalogo
from ...repositories import SomethingRepository
from ..base import CrudService
from fastapi import HTTPException
from .something_exceptions import SomethingAlreadyExistsException

class CatalogoService(CrudService[Catalogo, int]):
    def __init__(self, repository: SomethingRepository):
        super().__init__(repository)

    #async def find_by_name(self, name: str) -> Something:
        """
        Busca um Something pelo nome.
        """
    #    return await self.repository.find_by_name(name=name)
    
    async def validate_product_creation(self, seller_id: str, sku: str) -> None:
        """
        Valida se um produto pode ser criado verificando se já existe um produto com o mesmo seller_id e SKU.
        """
        try:
            # Tenta encontrar o produto pelo seller_id e SKU
            product_exist = await self.find_product(seller_id, sku)
        except Exception:  # Captura NotFoundException ou equivalente
            product_exist = None

        # Se o produto já existir, lança uma exceção
        if product_exist:
            raise SomethingAlreadyExistsException()