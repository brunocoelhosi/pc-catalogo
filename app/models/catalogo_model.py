from . import PersistableEntity


class Catalogo(PersistableEntity):
    seller_id: str
    sku: str
    product_name: str
