from unittest.mock import AsyncMock, MagicMock
import pytest

from app.common.exceptions import BadRequestException, NotFoundException
from app.models import CatalogoModel
from app.services import CatalogoService
from app.services.catalogo.catalogo_exceptions import ProductAlreadyExistsException, ProductNotExistException


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

    @pytest.mark.asyncio
    async def test_validate_product_exist_exception(self, service_with_mock, repository_mock):
        repository_mock.find_product = AsyncMock(side_effect=Exception("Erro inesperado"))
        with pytest.raises(ProductNotExistException):
            await service_with_mock.validate_product_exist("qualquer", "coisa")

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
