import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

#@pytest.mark.usefixtures("client_v2") OLD
@pytest.mark.usefixtures("mock_do_auth", "async_client")
class TestCatalogoRouterV2:

    @pytest.mark.asyncio    
    async def test_criar_produto(self, async_client: AsyncClient):
        novo_produto = {"seller_id": "magalu11", "sku": "magalu10", "name": "20"}
        resposta = await async_client.post("/seller/v2/catalogo", json=novo_produto, headers={"x-seller-id": "magalu11"})
        assert resposta.status_code == 201
        assert resposta.json()["seller_id"] == "magalu11"
        assert resposta.json()["sku"] == "magalu10"
        assert resposta.json()["name"] == "20"



    def test_criar_produto2(self, client_v2: TestClient):
        novo_produto = {"seller_id": "magalu11", "sku": "magalu10", "name": "20"}
        resposta = client_v2.post("/seller/v2/catalogo", json=novo_produto, headers={"seller-id": "magalu11"})
        assert resposta.status_code == 201
        assert resposta.json()["seller_id"] == "magalu11"
        assert resposta.json()["sku"] == "magalu10"
        assert resposta.json()["name"] == "20"

    def test_buscar_produto_sellerid_sku(self, client_v2: TestClient):
        # Cria o produto via API
        novo_produto = {"seller_id": "sellerapi1", "sku": "skuapi", "name": "tv"}
        resposta = client_v2.post("/seller/v2/catalogo", json=novo_produto, headers={"seller-id": "sellerapi1"})
        assert resposta.status_code == 201

        # Busca o produto via API
        resposta = client_v2.get("/seller/v2/catalogo/skuapi", headers={"seller-id": "sellerapi1"})
        assert resposta.status_code == 200
        data = resposta.json()
        assert data["seller_id"] == "sellerapi1"
        assert data["sku"] == "skuapi"

    def test_atualizar_catalogo(self, client_v2: TestClient):
        # Cria o produto via API
        novo_produto = {"seller_id": "magalu1", "sku": "ma1tv", "name": "tv50"}
        resposta = client_v2.post("/seller/v2/catalogo", json=novo_produto, headers={"seller-id": "magalu1"})
        assert resposta.status_code == 201

        # Atualiza o produto
        update = {"name": "tv60"}
        resposta = client_v2.put("/seller/v2/catalogo/ma1tv", json=update, headers={"seller-id": "magalu1"})
        assert resposta.status_code == 202
        assert resposta.json()["name"] == "tv60"

    def test_patch_catalogo(self, client_v2: TestClient):
        # Cria o produto via API
        novo_produto = {"seller_id": "magalu2", "sku": "ma2cel", "name": "celular"}
        resposta = client_v2.post("/seller/v2/catalogo", json=novo_produto, headers={"seller-id": "magalu2"})
        assert resposta.status_code == 201

        # Atualiza parcialmente o produto
        update = {"name": "tv70"}
        resposta = client_v2.patch("/seller/v2/catalogo/ma2cel", json=update, headers={"seller-id": "magalu2"})
        assert resposta.status_code == 202
        assert resposta.json()["name"] == "tv70"



    def test_deletar_catalogo(self, client_v2: TestClient):
        # Cria o produto via API
        novo_produto = {"seller_id": "magalu1", "sku": "ma1tv", "name": "tv50"}
        resposta = client_v2.post("/seller/v2/catalogo", json=novo_produto, headers={"seller-id": "magalu1"})
        assert resposta.status_code == 201

        # Deleta o produto
        resposta = client_v2.delete("/seller/v2/catalogo/ma1tv", headers={"seller-id": "magalu1"})
        assert resposta.status_code == 204
