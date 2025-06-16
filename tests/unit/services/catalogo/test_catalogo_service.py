from unittest.mock import AsyncMock, MagicMock
import pytest

from app.common.exceptions import BadRequestException, NotFoundException
from app.models import CatalogoModel
from app.services import CatalogoService
from app.services.catalogo.catalogo_exceptions import(
    ProductAlreadyExistsException,
    ProductNotExistException,
    LikeNotFoundException,
    ProductNameLengthException,
    SKULengthException,
    SellerIDException
    )
from app.api.common.schemas.pagination import Paginator
class FakeCursor:
    def __init__(self, items):
        self.items = items
        self._offset = 0
        self._limit = None
        self._sort = None

    def sort(self, field, order):
        self.items.sort(key=lambda x: x[field], reverse=(order == -1))
        return self

    def skip(self, offset):
        self._offset = offset
        return self

    def limit(self, limit):
        self._limit = limit
        return self

    async def to_list(self, length):
        result = self.items[self._offset:self._offset + (self._limit or length)]
        return result

    def __aiter__(self):
        self._iter = iter(self.items[self._offset:self._offset + (self._limit or len(self.items))])
        return self

    async def __anext__(self):
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration


@pytest.fixture
def repository_mock():
    mock = MagicMock()
    mock.create = AsyncMock(return_value=CatalogoModel(seller_id="seller1", sku="sku1", name="product1"))
    mock.validate_product_exist = AsyncMock(return_value=None)
    mock.find_product = AsyncMock(return_value=None)
    mock.find_by_seller_id = AsyncMock(return_value=[])
    mock.find = AsyncMock(return_value=[]) 
    mock.find_by_filter = AsyncMock(return_value=[])
    mock.delete_by_sellerid_sku = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def service_with_mock(repository_mock):
    return CatalogoService(repository=repository_mock)


class TestCatalogoService:

    @pytest.mark.asyncio
    async def test_create_catalogo_success(self, service_with_mock, repository_mock):
        catalogo_create = CatalogoModel(seller_id="magalu", sku="magatv", name="tv")
        repository_mock.create.return_value = catalogo_create

        created_catalogo = await service_with_mock.create(catalogo_create)

        assert created_catalogo is not None
        assert created_catalogo.seller_id == "magalu"
        assert created_catalogo.sku == "magatv"
        assert created_catalogo.name == "tv"
        repository_mock.create.assert_called_once_with(catalogo_create)

    @pytest.mark.asyncio
    async def test_create_product_already_exists(self, service_with_mock, repository_mock):
        catalogo_create = CatalogoModel(seller_id="123", sku="123", name="produto1")
        # Simula que o produto já existe
        repository_mock.find_product.return_value = catalogo_create

        with pytest.raises(ProductAlreadyExistsException):
            await service_with_mock.create(catalogo_create)

    """    @pytest.mark.asyncio
    async def test_validate_product_exist_exception(self, service_with_mock, repository_mock):
        repository_mock.find_product = AsyncMock(side_effect=Exception("Erro inesperado"))
        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_product_exist("qualquer", "coisa")"""

    @pytest.mark.asyncio
    async def test_validate_delete_success(self, service_with_mock, repository_mock):
        repository_mock.find_product.return_value = CatalogoModel(seller_id="123", sku="123", name="tv10")
        await service_with_mock.validate_delete("123", "123")
        repository_mock.find_product.assert_called_once_with("123", "123")

    @pytest.mark.asyncio
    async def test_validate_delete_exception(self, service_with_mock, repository_mock):
        repository_mock.find_product = AsyncMock(side_effect=Exception("Erro inesperado"))
        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_delete("qualquer", "coisa")

    @pytest.mark.asyncio
    async def test_validate_delete_not_found(self, service_with_mock, repository_mock):
        repository_mock.find_product.return_value = None
        with pytest.raises(NotFoundException):
            await service_with_mock.validate_delete("123", "999")
        repository_mock.find_product.assert_called_once_with("123", "999")

    @pytest.mark.asyncio
    async def test_delete_by_seller_id_and_sku_success(self, service_with_mock, repository_mock):
        repository_mock.find_product.return_value = CatalogoModel(seller_id="123", sku="123", name="produto1")
        repository_mock.delete_by_sellerid_sku.return_value = True

        await service_with_mock.delete_by_sellerid_sku("123", "123")

        repository_mock.find_product.assert_called_once_with("123", "123")
        repository_mock.delete_by_sellerid_sku.assert_called_once_with("123", "123")

    @pytest.mark.asyncio
    async def test_delete_by_seller_id_and_sku_not_found(self, service_with_mock, repository_mock):
        repository_mock.find_product.return_value = None

        with pytest.raises(ProductNotExistException):
            await service_with_mock.delete_by_sellerid_sku("123", "999")

        repository_mock.find_product.assert_called_once_with("123", "999")
        repository_mock.delete_by_sellerid_sku.assert_not_called()

    @pytest.mark.asyncio
    async def test_save(self, service_with_mock, repository_mock):
        catalogo = CatalogoModel(seller_id="seller1", sku="sku1", name="product1")
        repository_mock.create.return_value = catalogo

        saved_catalogo = await service_with_mock.save(catalogo)

        assert saved_catalogo is not None
        assert saved_catalogo.seller_id == "seller1"
        assert saved_catalogo.sku == "sku1"
        assert saved_catalogo.name == "product1"
        repository_mock.create.assert_called_once_with(catalogo)

    @pytest.mark.asyncio
    async def test_find_by_filter(self, service_with_mock, repository_mock, paginator: Paginator = None):
        catalogo1 = CatalogoModel(seller_id="seller1", sku="sku1", name="product1")
        catalogo2 = CatalogoModel(seller_id="seller1", sku="sku2", name="product2")
        repository_mock.find = AsyncMock(return_value=[catalogo1, catalogo2])

        result = await service_with_mock.find_by_filter("seller1", paginator)

        assert len(result) == 2
        assert result[0].sku == "sku1"
        assert result[1].sku == "sku2"
        repository_mock.find.assert_awaited_once_with(
            filters={"seller_id": "seller1"},
            limit=paginator.limit if paginator else 50,
            offset=paginator.offset if paginator else 0,
            sort=paginator.get_sort_order() if paginator else None
        )

    @pytest.mark.asyncio
    async def test_find_by_filter_no_results(self, service_with_mock, repository_mock):
        repository_mock.find = AsyncMock(return_value=[])

        with pytest.raises(NotFoundException):
            await service_with_mock.find_by_filter("seller1")

        repository_mock.find.assert_awaited_once_with(
            filters={"seller_id": "seller1"},
            limit=50,
            offset=0,
            sort=None
        )

    @pytest.mark.asyncio
    async def test_find_by_filter_with_name_like(self, service_with_mock, repository_mock, paginator: Paginator = None):
        catalogo1 = CatalogoModel(seller_id="seller1", sku="sku1", name="product1")
        catalogo2 = CatalogoModel(seller_id="seller1", sku="sku2", name="product2")
        repository_mock.find = AsyncMock(return_value=[catalogo1, catalogo2])

        paginator = Paginator(limit=10, offset=0, request_path="/fake-path")
        result = await service_with_mock.find_by_filter("seller1", paginator, name_like="product")

        assert len(result) == 2
        assert result[0].name == "product1"
        assert result[1].name == "product2"
        repository_mock.find.assert_awaited_once_with(
            filters={"seller_id": "seller1", "name": {"$regex": "product", "$options": "i"}},
            limit=10,
            offset=0,
            sort=paginator.get_sort_order() if paginator else None
        )

    @pytest.mark.asyncio
    async def test_find_by_filter_with_name_like_no_results(self, service_with_mock, repository_mock):
        repository_mock.find_by_filter.return_value = []

        paginator = Paginator(limit=10, offset=0, request_path="/fake-path")
        with pytest.raises(LikeNotFoundException):
            await service_with_mock.find_by_filter("seller1", paginator, name_like="nonexistent")

        repository_mock.find.assert_awaited_once_with(
            filters={"seller_id": "seller1", "name": {"$regex": "nonexistent", "$options": "i"}},
            limit=10,
            offset=0,
            sort=paginator.get_sort_order() if paginator else None
        )
    
    @pytest.mark.asyncio
    async def test_validate_product_exist_handles_exception(self, service_with_mock, repository_mock):

        repository_mock.find_product = AsyncMock(side_effect=Exception("Erro inesperado"))

        await service_with_mock.validate_product_exist("qualquer", "coisa")

        repository_mock.find_product.assert_called_once_with("qualquer", "coisa")
        
    @pytest.mark.asyncio
    async def test_validate_len_product_name_valid(self, service_with_mock):
        valid_names = ["Produto", "Produto com nome longo"]
        for name in valid_names:
            await service_with_mock.validate_len_product_name(name)

    @pytest.mark.asyncio
    async def test_validate_len_product_name_invalid(self, service_with_mock):
        invalid_names = ["", " ", "P", "A"*201]
        for name in invalid_names:
            with pytest.raises(ProductNameLengthException):
                await service_with_mock.validate_len_product_name(name)

    @pytest.mark.asyncio
    async def test_validate_len_sku_valid(self, service_with_mock):
        valid_sku = ["SKU", "SKUvalido"]
        for sku in valid_sku:
            await service_with_mock.validate_len_sku(sku)

    @pytest.mark.asyncio
    async def test_validate_len_sku_invalid(self, service_with_mock):
        invalid_skus = ["", " ", "A", None, 123, [], {}]
        for sku in invalid_skus:
            with pytest.raises(SKULengthException):
                await service_with_mock.validate_len_sku(sku)

    @pytest.mark.asyncio
    async def test_validate_len_seller_id_valid(self, service_with_mock):
        valid_seller_ids = ["seller1", "seller_123"]
        for seller_id in valid_seller_ids:
            await service_with_mock.validate_len_seller_id(seller_id)

    @pytest.mark.asyncio
    async def test_validate_len_seller_id_invalid(self, service_with_mock):
        invalid_seller_ids = ["", " ", "A", None, [], {}, "seller id with spaces"]
        with pytest.raises(SellerIDException):
                await service_with_mock.validate_len_seller_id(invalid_seller_ids)

    @pytest.mark.asyncio
    async def test_validate_patch_success(self, service_with_mock, repository_mock):
        seller_id = "seller1"
        sku = "sku1"
        patch_model = {"name": "Updated Product"}
        # Simula que o produto existe
        repository_mock.find_product.return_value = CatalogoModel(seller_id=seller_id, sku=sku, name="Old Product")

        result = await service_with_mock.validate_patch(seller_id, sku, patch_model)

        assert result == patch_model
        repository_mock.find_product.assert_called_once_with(seller_id, sku)

    @pytest.mark.asyncio
    async def test_validate_patch_not_found(self, service_with_mock, repository_mock):
        seller_id = "seller1"
        sku = "sku1"
        patch_model = {"name": "Updated Product"}
        # Simula que o produto NÃO existe
        repository_mock.find_product.return_value = None

        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_patch(seller_id, sku, patch_model)
        repository_mock.find_product.assert_called_once_with(seller_id, sku)


    @pytest.mark.asyncio
    async def test_validate_update_success(self, service_with_mock, repository_mock):
        seller_id = "seller1"
        sku = "sku1"
        catalogo = CatalogoModel(seller_id=seller_id, sku=sku, name="Updated Product")
        # Simula que o produto existe
        repository_mock.find_product.return_value = catalogo

        result = await service_with_mock.validate_update(seller_id, sku, catalogo)

        assert result == catalogo
        repository_mock.find_product.assert_called_once_with(seller_id, sku)

    @pytest.mark.asyncio
    async def test_validate_update_not_found(self, service_with_mock, repository_mock):
        seller_id = "seller1"
        sku = "sku1"
        catalogo = CatalogoModel(seller_id=seller_id, sku=sku, name="Updated Product")
        # Simula que o produto NÃO existe
        repository_mock.find_product.return_value = None

        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_update(seller_id, sku, catalogo)
        repository_mock.find_product.assert_called_once_with(seller_id, sku)

    @pytest.mark.asyncio
    async def test_validate_patch_handles_exception(self, service_with_mock, repository_mock):
        seller_id = "seller1"
        sku = "sku1"
        patch_model = {"name": "Updated Product"}
        # Simula que find_product lança uma exceção
        repository_mock.find_product = AsyncMock(side_effect=Exception("Erro inesperado"))

        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_patch(seller_id, sku, patch_model)
        repository_mock.find_product.assert_called_once_with(seller_id, sku)

    @pytest.mark.asyncio
    async def test_validate_update_handles_exception(self, service_with_mock, repository_mock):
        seller_id = "seller1"
        sku = "sku1"
        catalogo = CatalogoModel(seller_id=seller_id, sku=sku, name="Updated Product")
        # Simula que find_product lança uma exceção
        repository_mock.find_product = AsyncMock(side_effect=Exception("Erro inesperado"))

        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_update(seller_id, sku, catalogo)
        repository_mock.find_product.assert_called_once_with(seller_id, sku)