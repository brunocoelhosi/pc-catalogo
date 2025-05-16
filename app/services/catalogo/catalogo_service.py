from ...models import Catalogo
from ...repositories import SomethingRepository
from ..base import CrudService
from fastapi import HTTPException
from .something_exceptions import NoFieldsToUpdateException, SomethingAlreadyExistsException, ProductNotExistException,ProductNameLengthException,SellerIDException
from app.api.v1.schemas.something_schema import SomethingUpdate

class CatalogoService(CrudService[Catalogo, int]):
    def __init__(self, repository: SomethingRepository):
        super().__init__(repository)


    
    async def create(self, catalogo: Catalogo) -> Catalogo:
        """
        Cria um novo produto no catálogo.
        """
        
        #Valida o seller_id
        await self.validade_seller_id(catalogo.seller_id)

        # Verifica se o produto já existe
        await self.validate_product_exist(catalogo.seller_id, catalogo.sku)
        
        # Valida o tamanho do nome do produto
        await self.validate_len_product_name(catalogo.product_name)
        
        # Converte o seller_id para minúsculas
        catalogo.seller_id = catalogo.seller_id.lower()
        
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

    async def validate_product_exist(self, seller_id: str, sku: str) -> None:
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
        
    async def validade_seller_id(self, seller_id: str) -> None:
        """
        Valida o seller_id.
        """

        if len(seller_id) < 2 or seller_id == "":
            raise SellerIDException()
        
    async def update_product_partial(
        self,
        seller_id: str,
        sku: str,
        update_payload: SomethingUpdate
    ) -> Catalogo:
        """
        Atualiza parcialmente um produto no catálogo com base no seller_id e sku.
        """
        
        product_to_update = await self.find_product(seller_id, sku)
        
        update_data_for_service = update_payload.model_dump(exclude_unset=True)
        
        if not update_data_for_service:
            raise NoFieldsToUpdateException()
        if "product_name" in update_data_for_service and update_data_for_service["product_name"] is not None:
            await self.validate_len_product_name(update_data_for_service["product_name"])
            
        updated_product = await super().update(seller_id, update_payload)
        
        return updated_product
            
        