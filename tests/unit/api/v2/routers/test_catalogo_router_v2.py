import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, AsyncMock

@pytest.mark.usefixtures("client")
class TestCatalogoRouterV2:

    def test_buscar_produto_sellerid_sku(self, client: TestClient, test_catalogo):
        catalogo = test_catalogo[0]
        resposta = client.get(f"/seller/v2/catalogo/{catalogo.sku}", headers={"seller-id": catalogo.seller_id})
        assert resposta.status_code == 200
        data = resposta.json()
        assert data["seller_id"] == catalogo.seller_id
        assert data["sku"] == catalogo.sku

    def test_atualizar_catalogo(self, client: TestClient, test_catalogo):
        catalogo = test_catalogo[0]
        update = {"name": "tv60"}
        resposta = client.put(f"/seller/v2/catalogo/{catalogo.sku}", json=update, headers={"seller-id": catalogo.seller_id})
        assert resposta.status_code == 200
        assert resposta.json()["name"] == "tv60"

    def test_patch_catalogo(self, client: TestClient, test_catalogo):
        catalogo = test_catalogo[0]
        update = {"name": "tv70"}
        resposta = client.patch(f"/seller/v2/catalogo/{catalogo.sku}", json=update, headers={"seller-id": catalogo.seller_id})
        assert resposta.status_code == 200
        assert resposta.json()["name"] == "tv70"

    def test_patch_catalogo_nenhuma_alteracao(self, client: TestClient, test_catalogo):
        catalogo = test_catalogo[0]
        # Envia exatamente o mesmo dado já existente
        update = {"name": catalogo.name}
        resposta = client.patch(
            f"/seller/v2/catalogo/{catalogo.sku}",
            json=update,
            headers={"seller-id": catalogo.seller_id}
        )
        assert resposta.status_code == 404
        assert resposta.json()["detail"] == "Produto não encontrado ou nada foi alterado"



    def test_criar_produto(self, client: TestClient):
        novo_produto = {"seller_id": "magalu10", "sku": "magalu10", "name": "20"}
        resposta = client.post("/seller/v2/catalogo", json=novo_produto, headers={"seller-id": "magalu10"})
        assert resposta.status_code == 201
        assert resposta.json()["seller_id"] == "magalu10"
        assert resposta.json()["sku"] == "magalu10"
        assert resposta.json()["name"] == "20"


    def test_deletar_catalogo(self, client: TestClient, test_catalogo):
        catalogo = test_catalogo[0]
        resposta = client.delete(f"/seller/v2/catalogo/{catalogo.sku}", headers={"seller-id": catalogo.seller_id})
        assert resposta.status_code == 204
