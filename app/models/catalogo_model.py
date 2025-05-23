from dataclasses import Field
from . import PersistableEntity


class Catalogo(PersistableEntity):
    seller_id: str = Field(..., regex=r'^[a-z0-9]+$', description="Só letras minúsculas e números")
    sku: str = Field(..., regex=r'^[A-Za-z0-9]+$', description="Só letras e números, sem espaços")
    product_name: str = Field(..., min_length=2, max_length=200)
