import pytest
from app.common.exceptions import ConflictException
from app.services.catalogo.catalogo_exceptions_v1 import (
    ProductAlreadyExistsException,
    ProductNotExistException,
    ProductNameLengthException,
    SKULengthException,
    SellerIDException,
    NoFieldsToUpdateException,
    SellerIDNotExistException,
    LikeNotFoundException
)

class TestCatalogoExceptionsV1:

    @pytest.mark.asyncio
    async def test_product_exist(ConflictException):
        with pytest.raises(ProductAlreadyExistsException):
            raise ProductAlreadyExistsException()

    @pytest.mark.asyncio
    async def test_product_not_exist(ConflictException):
        with pytest.raises(ProductNotExistException):
            raise ProductNotExistException()
        
    @pytest.mark.asyncio
    async def test_product_name_length(ConflictException):
        with pytest.raises(ProductNameLengthException):
            raise ProductNameLengthException()
        
    @pytest.mark.asyncio
    async def test_sku_length(ConflictException):
        with pytest.raises(SKULengthException):
            raise SKULengthException()
        
    @pytest.mark.asyncio
    async def test_seller_id_length(ConflictException):
        with pytest.raises(SellerIDException):
            raise SellerIDException()
        
    @pytest.mark.asyncio
    async def test_no_fields_to_update(ConflictException):
        with pytest.raises(NoFieldsToUpdateException):
            raise NoFieldsToUpdateException()
        
    @pytest.mark.asyncio
    async def test_seller_id_not_exist(ConflictException):
        with pytest.raises(SellerIDNotExistException):
            raise SellerIDNotExistException()
        
        
    @pytest.mark.asyncio
    async def test_like_not_found(ConflictException):
        with pytest.raises(LikeNotFoundException):
            raise LikeNotFoundException()
