import pytest

from app.models import CatalogoModel
#from app.repositories import CatalogoRepository

from app.repositories.base.mongo_catalogo_repository import MongoCatalogoRepository


from unittest.mock import MagicMock, AsyncMock
from unittest.mock import MagicMock, AsyncMock

import sys


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
            return next(self._iter)  # <-- deve ser um dict
        except StopIteration:
            raise StopAsyncIteration
        
class TestCatalogoRepository:
    @pytest.fixture
    def repository(self):
        repo = MongoCatalogoRepository(
            client=MagicMock(),
            collection_name="catalogo",
            model_class=CatalogoModel
        )
        repo.memory = [
            {"seller_id": "123", "sku": "123", "name": "Produto 1"},
            {"seller_id": "1234", "sku": "1234", "name": "Produto 14"},
        ]
        # Mock collection methods
        repo.collection = MagicMock()
        repo.collection.find_one = AsyncMock(
            side_effect=lambda f: next(
                (
                    item for item in repo.memory
                    if item["seller_id"] == f.get("seller_id") and
                       (("sku" not in f) or item["sku"] == f.get("sku"))
                ),
                None
            )
        )
        repo.collection.find = MagicMock(
            side_effect=lambda f: FakeCursor([item for item in repo.memory if all(item[k] == v for k, v in f.items())])
        )
        repo.collection.insert_one = AsyncMock(
            side_effect=lambda doc: repo.memory.append(doc) or MagicMock(inserted_id="fake_id")
        )
        repo.collection.find_one_and_update = AsyncMock(
            side_effect=lambda f, u, return_document: {**f, **u["$set"]}
        )
        repo.collection.delete_many = AsyncMock(
            side_effect=lambda f: MagicMock(deleted_count=1)
        )
        return repo

    @pytest.mark.asyncio
    async def test_find_product(self, repository):
        """Deve encontrar um produto existente pelo seller_id e sku."""
        print('teste')
        result_dict = await repository.find_product("123", "123")

        assert result_dict is not None
        assert result_dict.seller_id == "123"
        assert result_dict.sku == "123"
        assert result_dict.name == "Produto 1"

    @pytest.mark.asyncio
    async def test_create_base(self, repository):
        entity = CatalogoModel(seller_id="999", sku="sku999", name="Produto 999")
        created = await repository.create(entity)
        assert created.seller_id == "999"
        assert created.sku == "sku999"
        assert created.name == "Produto 999"

    @pytest.mark.asyncio
    async def test_find(self, repository):

        """Deve encontrar um produto existente pelo seller_id e sku."""
        result_list = await repository.find({"seller_id": "123", "sku": "123"})
        assert result_list is not None
        assert len(result_list) > 0
        result = result_list[0]
        assert result.seller_id == "123"
        assert result.sku == "123"
        assert result.name == "Produto 1"

    @pytest.mark.asyncio
    async def test_find_with_sort(self, repository):
        print('rota')
        print(sys.modules["app.repositories.catalogo_repository"])
        #print(repository.__class__)

        result_list = await repository.find(
            {"seller_id": "123", "sku": "123"},
            sort={"name": 1}
        )
        assert result_list is not None
        assert len(result_list) > 0
        result = result_list[0]
        assert result.seller_id == "123"


    @pytest.mark.asyncio
    async def test_create(self, repository):
        """Deve criar um novo preço e permitir sua busca."""
        novo_produto = CatalogoModel(seller_id="32", sku="caa", name="produtonovo1")
        produto_criado = await repository.create(novo_produto)

        assert produto_criado is not None
        assert produto_criado.seller_id == "32"
        assert produto_criado.sku == "caa"
        assert produto_criado.name == "produtonovo1"
        assert produto_criado.created_at is not None    

        # Verifica se pode ser encontrado no repositório
        result_dict = await repository.find_product("32", "caa")
        assert result_dict is not None
        assert result_dict.seller_id == "32"
        assert result_dict.sku  == "caa"



    @pytest.mark.asyncio
    async def test_update(self, repository):
        entity = CatalogoModel(seller_id="123", sku="123", name="Produto Atualizado")
        updated = await repository.update({"seller_id": "123", "sku": "123"}, entity)
        assert updated.seller_id == "123"
        assert updated.name == "Produto Atualizado"

    @pytest.mark.asyncio
    async def test_delete(self, repository):
        result = await repository.delete({"seller_id": "123", "sku": "123"})
        assert result is True

    @pytest.mark.asyncio
    async def test_find_one_found(self, repository):
        result = await repository.find_one({"seller_id": "123", "sku": "123"})
        assert result is not None

    @pytest.mark.asyncio
    async def test_find_one_not_found(self, repository):
        result = await repository.find_one({"seller_id": "notfound", "sku": "notfound"})
        assert result is None

    @pytest.mark.asyncio
    async def test_find_by_sellerid_sku(self, repository):
        result = await repository.find_by_sellerid_sku("123", "123")
        assert result is not None

    @pytest.mark.asyncio
    async def test_find_by_seller_id(self, repository):
        result = await repository.find_by_seller_id("123")
        assert result is not None
        
    @pytest.mark.asyncio
    async def test_find_by_seller_id_not_found(self, repository):
        result = await repository.find_by_seller_id("notfound")
        assert result is None

    @pytest.mark.asyncio
    async def test_update_by_sellerid_sku(self, repository):
        entity = CatalogoModel(seller_id="123", sku="123", name="Novo Nome")
        updated = await repository.update_by_sellerid_sku("123", "123", entity)
        assert updated is not None

    @pytest.mark.asyncio
    async def test_patch_by_sellerid_sku(self, repository):
        patch = {"name": "Nome Patch"}
        updated = await repository.patch_by_sellerid_sku("123", "123", patch)
        assert updated is not None

    @pytest.mark.asyncio
    async def test_delete_by_sellerid_sku(self, repository):
        deleted = await repository.delete_by_sellerid_sku("123", "123")
        assert deleted is True

    @pytest.mark.asyncio
    async def test_build_sellerid_sku_filter(self,repository): 
        build = repository.build_sellerid_sku_filter("123", "123")
        assert  build is not None

    @pytest.mark.asyncio
    async def test_build_sellerid_filter(self, repository):
        build = repository.build_sellerid_filter("123")
        assert build is not None