from . import PersistableEntity


class Something(PersistableEntity):
    seller_id: str
    sku: str
    product_name: str
