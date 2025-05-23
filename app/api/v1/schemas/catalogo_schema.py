from typing import Optional
from app.api.common.schemas import ResponseEntity, SchemaType


class CatalogoSchema(SchemaType):
    seller_id: str
    sku: str
    product_name: str


class CatalogoResponse(CatalogoSchema, ResponseEntity):
    """Resposta adicionando"""


class CatalogoCreate(CatalogoSchema):
    seller_id: str
    sku: str
    product_name: str


class CatalogoUpdate(SchemaType):
    """Permite apenas a atualização do nome do produto"""
    product_name: Optional[str] = None
