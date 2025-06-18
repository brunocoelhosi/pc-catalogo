import pytest
from app.models import CatalogoModel

class TestMongoCatalogoRepository:

    @pytest.mark.asyncio
    async def test_create_and_find(self, repository):
        produto = CatalogoModel(seller_id="test1", sku="sku1", name="Produto Teste")
        criado = await repository.create(produto)
        assert criado.seller_id == "test1"
        assert criado.sku == "sku1"

        encontrado = await repository.find_product("test1", "sku1")
        assert encontrado is not None
        assert encontrado.seller_id == "test1"

    @pytest.mark.asyncio
    async def test_find_product(self, repository):
        """Deve encontrar um produto existente pelo seller_id e sku."""
        produto = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(produto)

        result = await repository.find_product("123", "123")
        assert result is not None
        assert result.seller_id == "123"
        assert result.sku == "123"
        assert result.name == "Produto 1"

    @pytest.mark.asyncio
    async def test_find(self, repository):

        produto = CatalogoModel(seller_id="1234", sku="1234", name="Produto 2")
        await repository.create(produto)

        result = await repository.find({"seller_id": "1234", "sku": "1234"})
        assert result is not None
        assert len(result) > 0
        result = result[0]
        assert result.seller_id == "1234"
        assert result.sku == "1234"
        assert result.name == "Produto 2"

    @pytest.mark.asyncio
    async def test_find_with_sort(self, repository):

        produto = CatalogoModel(seller_id="magalu", sku="matv", name="tv")
        await repository.create(produto)

        result_list = await repository.find(
            {"seller_id": "magalu", "sku": "matv"},
            sort={"name": 1}
        )
        assert result_list is not None
        assert len(result_list) > 0
        result = result_list[0]
        assert result.seller_id == "magalu"

    @pytest.mark.asyncio
    async def test_delete(self, repository):
        produto = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(produto)

        result = await repository.delete({"seller_id": "123", "sku": "123"})
        assert result is True

    @pytest.mark.asyncio
    async def test_update(self, repository):
        # Cria o produto original
        produto = CatalogoModel(seller_id="123", sku="123", name="Produto1")
        await repository.create(produto)

        # Cria um novo objeto com o mesmo seller_id e sku, mas com o novo name
        produto_atualizado = CatalogoModel(seller_id="123", sku="123", name="Produto2")
        updated = await repository.update({"seller_id": "123", "sku": "123"}, produto_atualizado)

        assert updated.seller_id == "123"
        assert updated.sku == "123"
        assert updated.name == "Produto2"

    @pytest.mark.asyncio
    async def test_update_by_sellerid_sku(self, repository):
        # Cria o produto original com seller_id="1234" e sku="1234"
        produto = CatalogoModel(seller_id="1234", sku="1234", name="produto2")
        await repository.create(produto)

        # Atualiza o produto (mantendo seller_id e sku, mudando apenas o name)
        produto_atualizado = CatalogoModel(seller_id="1234", sku="1234", name="produto3")
        updated = await repository.update_by_sellerid_sku("1234", "1234", produto_atualizado)

        assert updated is not None
        assert updated.sku == "1234"
        assert updated.seller_id == "1234"
        assert updated.name == "produto3"

    @pytest.mark.asyncio
    async def test_update_document_not_found(self, repository):
        product = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(product)
        
        result = await repository.update_by_sellerid_sku("idnotexist", "aaa", product)
        assert result is None

    @pytest.mark.asyncio
    async def test_build_sellerid_sku_filter(self,repository): 
        build = repository.build_sellerid_sku_filter("123", "123")
        assert  build is not None

    @pytest.mark.asyncio
    async def test_build_sellerid_filter(self, repository):
        build = repository.build_sellerid_filter("123")
        assert build is not None

    @pytest.mark.asyncio
    async def test_find_one_found(self, repository):
        produto = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(produto)

        result = await repository.find_one({"seller_id": "123", "sku": "123"})
        assert result is not None
        assert result.seller_id == "123"
        assert result.sku == "123"
        assert result.name == "Produto 1"   
    
    @pytest.mark.asyncio
    async def test_find_one_not_found(self, repository):
        produto = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(produto)

        result = await repository.find_one({"seller_id": "notfound", "sku": "notfound"})
        assert result is None

    @pytest.mark.asyncio
    async def test_patch_by_sellerid_sku(self, repository):
        produto = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(produto)

        patch = {"name": "Produto Atualizado"}
        updated = await repository.patch_by_sellerid_sku("123", "123", patch)
        assert updated is not None
        assert updated.seller_id == "123"
        assert updated.sku == "123"
        assert updated.name == "Produto Atualizado"

    @pytest.mark.asyncio
    async def test_find_by_sellerid_sku(self, repository):
        product = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(product)
        result = await repository.find_by_sellerid_sku("123", "123")
        assert result is not None
        assert result.seller_id == "123"
        assert result.sku == "123"

    @pytest.mark.asyncio
    async def test_find_by_seller_id(self, repository):
        product = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(product)
        result = await repository.find_by_seller_id("123")
        assert result is not None
        
    @pytest.mark.asyncio
    async def test_find_by_seller_id_not_found(self, repository):
        product = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(product)
        result = await repository.find_by_seller_id("notfound")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_by_sellerid_sku(self, repository):
        product = CatalogoModel(seller_id="123", sku="123", name="Produto 1")
        await repository.create(product)
        deleted = await repository.delete_by_sellerid_sku("123", "123")
        assert deleted is True
    
    