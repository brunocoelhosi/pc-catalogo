from ...models import Catalogo
from ...repositories import SomethingRepository
from ..base import CrudService
from fastapi import HTTPException
from .something_exceptions import NoFieldsToUpdateException, SomethingAlreadyExistsException, ProductNotExistException,ProductNameLengthException,SellerIDException, SKULengthException, SellerIDNotExistException
from app.api.v1.schemas.something_schema import SomethingUpdate

class CatalogoService(CrudService[Catalogo, int]):
    def __init__(self, repository: SomethingRepository):
        super().__init__(repository)


    async def create(self, catalogo: Catalogo) -> Catalogo:
        """
        Cria um novo produto no catálogo.
        """
        await self.validate(catalogo)
        await self.review(catalogo)
        return await self.save(catalogo)

    async def validate(self, catalogo: Catalogo) -> None:

        await self.validade_len_seller_id(catalogo.seller_id)
        await self.validade_len_sku(catalogo.sku)
        await self.validate_len_product_name(catalogo.product_name)

    async def review(self, catalogo: Catalogo) -> None:
        # Converte e limpa campos
        catalogo.seller_id = catalogo.seller_id.lower().strip()
        catalogo.sku = catalogo.sku.strip()
        catalogo.product_name = catalogo.product_name.strip()
        # Verifica se o produto já existe
        await self.validate_product_exist(catalogo.seller_id, catalogo.sku)

    async def save(self, catalogo: Catalogo) -> Catalogo:
        return await super().create(catalogo)
    
    async def delete_product(self, seller_id: str, sku: str) -> None:
        """
        Deleta um produto do catálogo.
        """
        seller_id = seller_id.lower()
        product = await self.find_product(seller_id, sku)
        if product is None:
            raise ProductNotExistException()

        await self.repository.delete_product(product)

    async def find_by_seller_id(self, seller_id):
        """
        Busca todos os produtos no catálogo com base no seller_id.
        """
        seller_id = seller_id.lower()
        result = await super().find_by_seller_id(seller_id)
        if not result:
            raise SellerIDNotExistException()
        return result

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
        is_only_whitespace = lambda s: not s or s.isspace()

        if len(product_name) < 2 or len(product_name) > 200 or product_name == "" or is_only_whitespace(product_name):
            raise ProductNameLengthException()
        
    async def validade_len_sku(self, sku: str) -> None:
        """
        Valida o SKU.
        """
        is_only_whitespace = lambda s: not s or s.isspace()

        if len(sku) < 2 or sku == "" or is_only_whitespace(sku):
            raise SKULengthException()
        
    async def validade_len_seller_id(self, seller_id: str) -> None:
        """
        Valida o seller_id.
        """
        is_only_whitespace = lambda s: not s or s.isspace()

        if len(seller_id) < 2 or seller_id == "" or is_only_whitespace(seller_id):
            raise SellerIDException()
        
    async def update_product_partial(self, seller_id: str, sku: str, update_payload: SomethingUpdate) -> Catalogo:
        """
        Atualiza parcialmente um produto no catálogo com base no seller_id e sku.
        """
        seller_id = seller_id.lower()

        # Busca o produto atual
        product_to_update = await self.find_product(seller_id, sku)

        if not product_to_update:
            raise ProductNotExistException()

        #exclude_unset=True: somente os campos que foram enviados no payload serão atualizados
        update_data_for_service = update_payload.model_dump(exclude_unset=True)

        if not update_data_for_service:
            raise NoFieldsToUpdateException()

        # Verifica se os dados enviados são iguais aos já existentes
        is_same = True
        for key, value in update_data_for_service.items():
            if getattr(product_to_update, key, None) != value:
                is_same = False
                break

        if is_same:
            raise NoFieldsToUpdateException()

        if "product_name" in update_data_for_service and update_data_for_service["product_name"] is not None:
            await self.validate_len_product_name(update_data_for_service["product_name"])

        updated_product = await super().update(seller_id, update_payload)
        return updated_product

