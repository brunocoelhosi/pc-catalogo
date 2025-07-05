from app.api.common.schemas.pagination import Paginator
from ...models import CatalogoModel
from ...repositories import CatalogoRepository
from ..base import CrudService
from .catalogo_exceptions import ( 
    NoFieldsToUpdateException, 
    ProductAlreadyExistsException, 
    ProductNotExistException,
    ProductNameLengthException,
    SellerIDException, 
    SKULengthException, 
    SellerIDNotExistException, 
    LikeNotFoundException,
    ProductNameNotFoundException
)
from dependency_injector.wiring import inject, Provide
from app.api.v1.schemas.catalogo_schema import CatalogoUpdate
from typing import TypeVar
from app.integrations.cache.redis_asyncio_adapter import RedisAsyncioAdapter
from app.worker.description.creating_product_description import CreatingProductDescription

T = TypeVar("T")

from pclogging import LoggingBuilder

LoggingBuilder.init(log_level="DEBUG")

logger = LoggingBuilder.get_logger(__name__)

class CatalogoService(CrudService[CatalogoModel, int]):

    redis_adapter: RedisAsyncioAdapter

    def __init__(self, repository: CatalogoRepository, redis_adapter: RedisAsyncioAdapter):
        super().__init__(repository)
        self.redis_adapter = redis_adapter

    @inject
    async def create(self,
                    catalogo: CatalogoModel,
                    creating_product_description: CreatingProductDescription = Provide["creating_product_description"],
                    ) -> CatalogoModel:
        """
        Cria um novo produto no catálogo.
        """
        await self.review(catalogo)
        await self.validate(catalogo)
        # Gera a descrição usando IA
        description_data = await creating_product_description.create_description(catalogo)
        # Se a IA retornar um dicionário com a chave "description"
        if description_data and "description" in description_data:
            catalogo.description = description_data["description"]
        else:
            catalogo.description = ""
        return await self.save(catalogo)
    
    async def validate(self, catalogo: CatalogoModel) -> None:
        
        await self.validate_len_seller_id(catalogo.seller_id)
        await self.validate_len_sku(catalogo.sku)
        await self.validate_len_product_name(catalogo.name)
        await self.validate_product_exist(catalogo.seller_id, catalogo.sku)

    async def review(self, catalogo: CatalogoModel) -> None:
        # Converte e limpa campos
        catalogo.seller_id = catalogo.seller_id.lower().strip()
        catalogo.sku = catalogo.sku.strip()
        catalogo.name = catalogo.name.strip()

    async def save(self, catalogo: CatalogoModel) -> CatalogoModel:
        return await super().create(catalogo)
    
    async def update_by_sellerid_sku(self, seller_id: str, sku: str, model: T) -> T:

        if not model.name or not model.name.strip():
            raise ProductNameNotFoundException()
        
        model = await self.validate_update(seller_id, sku, model)
        model = await self.repository.update_by_sellerid_sku(seller_id, sku, model)
        #Remove produto do cache após atualização
        cache_key = f"produto:{seller_id}:{sku}"
        await self.redis_adapter.delete(cache_key)
        return model
    
    async def delete_by_sellerid_sku(self, seller_id: str, sku: str, raises_exception: bool = True) -> bool:
        """ 
        Deleta um produto do catálogo com base no seller_id e SKU.
        """
        await self.validate_delete(seller_id, sku)
        deleted = await self.repository.delete_by_sellerid_sku(seller_id, sku)
        #Remove produto do cache após deleção
        cache_key = f"produto:{seller_id}:{sku}"
        await self.redis_adapter.delete(cache_key)
        return deleted
    
    async def patch_by_sellerid_sku(self, seller_id: str, sku: str, patch_model: dict) -> T:

        await self.find_by_seller_id(seller_id)
        patch_model = await self.validate_patch(seller_id, sku, patch_model)
        model = await self.repository.patch_by_sellerid_sku(seller_id, sku, patch_model)
        #Remove produto do cache após atualização
        cache_key = f"produto:{seller_id}:{sku}"
        await self.redis_adapter.delete(cache_key)

        return model
    
    async def find_by_filter(self, seller_id: str, paginator: Paginator = None, name_like: str = None) -> list[CatalogoModel]:
        """ 
        Busca produtos no catálogo filtrando por seller_id e opcionalmente por nome (like).
        """
        filters = {"seller_id": seller_id.lower()}
        if name_like:
            filters["name"] = {"$regex": name_like, "$options": "i"}
        limit = paginator.limit if paginator else 50
        offset = paginator.offset if paginator else 0
        sort = paginator.get_sort_order() if paginator else None
        result = await self.repository.find(filters=filters, limit=limit, offset=offset, sort=sort)
        if not result:
            if name_like:
                raise LikeNotFoundException()
            else:
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
            raise ProductAlreadyExistsException()
        
    async def validate_len_product_name(self, name: str) -> None:
        """
        Valida o tamanho do nome do produto.
        """
        if not name or name.strip() == "" or not (2 <= len(name.strip()) <= 200):
            raise ProductNameLengthException()

    async def validate_len_sku(self, sku: str) -> None:
        """
        Valida o SKU.
        """
        if not isinstance(sku, str) or not sku.strip() or len(sku.strip()) < 2:
        
            raise SKULengthException()
        
    async def validate_len_seller_id(self, seller_id: str) -> None:
        """
        Valida o seller_id.
        """
        if not isinstance(seller_id, str) or not seller_id.strip() or len(seller_id.strip()) < 2:
            raise SellerIDException()

    async def validate_patch(self, seller_id, sku, patch_model) -> dict:

        try:
            product_exist = await self.find_product(seller_id, sku)
        except Exception:
            product_exist = None

        if not product_exist:
            raise ProductNotExistException()

        return patch_model
    
    async def validate_update(self, seller_id: str, sku: str, catalogo: CatalogoModel) -> CatalogoModel:
        try:
            product_exist = await self.find_product(seller_id, sku)
        except Exception:
            product_exist = None

        if not product_exist:
            raise ProductNotExistException()

        return catalogo
            
    async def validate_delete(self, seller_id: str, sku: str):
        try:
            product_exist = await self.find_product(seller_id, sku)
        except Exception:
            product_exist = None

        if not product_exist:
            raise ProductNotExistException()
        
    async def find_by_sellerid_sku(self, seller_id: str, sku: str, raises_exception: bool = True) -> T | None:
        logger.debug(f"Buscando produto no CACHE -> seller_id: {seller_id}, sku: {sku}")
        cache_key = f"produto:{seller_id}:{sku}"
        cached = await self.find_product_in_cache(seller_id, sku, cache_key)

        if cached is not None:
            return cached
        
        try:
            product_exist = await self.repository.find_by_sellerid_sku(seller_id, sku)
        except Exception:
            product_exist = None

        if not product_exist:
            if raises_exception:
                raise ProductNotExistException()
            return None

        # Cache the product after fetching from repository
        try:
            # Assuming product_exist has a model_dump method (like a Pydantic model)
            await self.redis_adapter.set_json(cache_key, product_exist.model_dump(mode="json"), expires_in_seconds=300)
        except Exception as e:
            logger.warning(f"Falha ao salvar produto no cache: {e}")

        return product_exist

    async def find_product_in_cache(self, seller_id: str, sku: str, cache_key: str) -> dict:
        """
        Busca um preço pelo seller_id e sku, utilizando cache.

        :param seller_id: Identificador do vendedor.
        :param sku: Código do produto.
        :return: Instância de Preco encontrada.
        :raises NotFoundException: Se não encontrar o preço.
        """
        cached = await self.redis_adapter.get_json(cache_key)
        if cached is not None:
            logger.debug(f"🔄 Produto encontrado no CACHE -> seller_id: {seller_id}, sku: {sku}")
            return CatalogoModel.model_validate(cached)
