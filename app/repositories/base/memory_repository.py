from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException

from .async_crud_repository import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=int | str)


class AsyncMemoryRepository(AsyncCrudRepository[T, ID], Generic[T, ID]):

    def __init__(self):
        super().__init__()
        self.memory = []
        # Deveria passar dinamco

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(by_alias=True)
        entity_dict["created_at"] = utcnow()

        self.memory.append(entity)

        return entity_dict

    #Busca pelo ID do seller
    async def find_by_id(self, entity_id: ID) -> Optional[T]:

        result = next((r for r in self.memory if r.seller == entity_id), None)
        if result:
            return result

        raise NotFoundException()
    
    async def find_by_sku(self, sku: str) -> Optional[T]:
        # Busca pelo SKU no repositório em memória
        result = next((r for r in self.memory if r.sku == sku), None)
        if result:
            return result
        raise NotFoundException()

    async def find_product(self, id: str, sku: str) -> Optional[T]:
        # Busca por um produto unico seller + sku
        
        id = id.lower()

        result = next((r for r in self.memory if r.sku == sku and r.seller_id == id), None)
        if result:
            return result
        raise NotFoundException("Produto não encontrado.")
    
    async def delete_product(self, product) -> None:

        if product in self.memory:
            self.memory.remove(product)
            return {"message": "Product deleted successfully"}
        
        raise NotFoundException()
    

    async def update(self, entity_id: ID, entity_update_payload) -> T:
        index_toupdate = -1
        found_entity = None
        for i, item in enumerate(self.memory):
            if hasattr(item, "seller_id") and item.seller_id == entity_id:
                index_to_update = i
                found_entity = item
                break
            elif hasattr(item, 'id') and item.id == entity_id:
                index_to_update = i
                found_entity = item
                break
        if found_entity is None:
            raise NotFoundException(f"Entidade com ID {entity_id} não encontrada.")
        
        update_data = entity_update_payload.model_dump(exclude_unset=True)
        
        if not update_data:
            return found_entity
        
        for key, value in update_data.items():
            if hasattr(found_entity, key):
                setattr(found_entity, key, value)
            
        if hasattr(found_entity, "updated_at"):
            setattr(found_entity, "updated_at", utcnow())
            
        return found_entity

    async def delete_by_id(self, entity_id: ID) -> None:
        # XXX TODO
        current_document = await self.find_by_id(entity_id)
        if not current_document:
            raise NotFoundException()
        
    async def find(self, filters: dict, limit: int = 10, offset: int = 0, sort: Optional[dict] = None) -> List[T]:

        filtered_list = [
            data
            for data in self.memory
                
            # TODO Criar filtro
        ]

        # XXX TODO Falta ordenar    

        entities = []
        for document in filtered_list:
            entities.append(document)
        return entities
       
        
