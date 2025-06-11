import pytest
from fastapi.testclient import TestClient


@pytest.mark.usefixtures("client_v1")
class TestCatalogoRouterV1:
    def test_listar_produtos(self, client_v1: TestClient):
        resposta = client_v1.get("/seller/v1/catalogo")
        assert resposta.status_code == 200
        assert "results" in resposta.json()

    def test_criar_produto(self, client_v1: TestClient):
        novo_produto = {"seller_id": "magalu1", "sku": "ma1tv", "name": "tv50"}
        resposta = client_v1.post("/seller/v1/catalogo", json=novo_produto)
        assert resposta.status_code == 201
        assert resposta.json()["seller_id"] == "magalu1"
        assert resposta.json()["sku"] == "ma1tv"
        assert resposta.json()["name"] == "tv50"

    def test_buscar_produto_por_seller_e_sku(self, client_v1: TestClient, test_catalogo_v1):
        produto = test_catalogo_v1[0]
        resposta = client_v1.get(f"/seller/v1/catalogo/{produto.seller_id}/{produto.sku}")
        assert resposta.status_code == 200
        assert resposta.json()["seller_id"] == produto.seller_id
        assert resposta.json()["sku"] == produto.sku

    def test_patch_produto(self, client_v1: TestClient, test_catalogo_v1):
        produto = test_catalogo_v1[0]
        update = {"name": "celular1"}
        resposta = client_v1.patch(f"/seller/v1/catalogo/{produto.seller_id}/{produto.sku}", json=update)
        assert resposta.status_code == 200
        assert resposta.json()["name"] == "celular1"

    def test_patch_produto_sem_alteracao(self, client_v1: TestClient, test_catalogo_v1):
        produto = test_catalogo_v1[0]
        # Envia exatamente o mesmo dado já existente
        patch = {"name": produto.name}
        resposta = client_v1.patch(f"/seller/v1/catalogo/{produto.seller_id}/{produto.sku}", json=patch)
        assert resposta.status_code == 404
        #assert resposta.json()["detail"] == "Produto não encontrado ou nada foi alterado"

    def test_deletar_produto(self, client_v1: TestClient, test_catalogo_v1):
        produto = test_catalogo_v1[0]
        resposta = client_v1.delete(f"/seller/v1/catalogo/{produto.seller_id}/{produto.sku}")
        assert resposta.status_code == 204



