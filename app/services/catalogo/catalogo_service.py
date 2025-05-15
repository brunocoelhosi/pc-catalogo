from ...models import Catalogo
from ...repositories import SomethingRepository
from ..base import CrudService
from fastapi import HTTPException
from .something_exceptions import SomethingAlreadyExistsException, ProductNotExistException,ProductNameLengthException

class CatalogoService(CrudService[Catalogo, int]):
    def __init__(self, repository: SomethingRepository):
        super().__init__(repository)


    
    async def create(self, catalogo: Catalogo) -> Catalogo:
        """
        Cria um novo produto no catálogo.
        """
        # Verifica se o produto já existe
        await self.validate_product_creation(catalogo.seller_id, catalogo.sku)
        
        # Valida o tamanho do nome do produto
        await self.validate_len_product_name(catalogo.product_name)

        # Cria o produto
        resp = await super().create(catalogo)
        return resp
    
    async def delete_product(self, seller_id: str, sku: str) -> None:
        """
        Deleta um produto do catálogo.
        """
        try:
            # Tenta encontrar o produto pelo seller_id e SKU
            product = await self.find_product(seller_id, sku)
        except Exception:  # Captura NotFoundException ou equivalente
            product = None

        if product is None:
            raise ProductNotExistException()
        
        # Deleta o produto
        await self.repository.delete_product(product)

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

    async def validate_len_product_name(self, product_name: str) -> None:
        """
        Valida o tamanho do nome do produto.
        """
        if len(product_name) < 2 or len(product_name) > 15 or product_name == "":
            raise ProductNameLengthException()