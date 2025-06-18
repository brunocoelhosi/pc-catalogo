from datetime import datetime

import pytest
from pydantic import ValidationError

from app.models import CatalogoModel

class TestCatalogoModel:
    def test_create_catalogo(self):
        """Testa a criação de uma instância do Catalogo com os campos obrigatórios."""
        catalogo = CatalogoModel(seller_id="magalu1", sku="ma1gela", name="geladeira")

        assert catalogo.seller_id == "magalu1"
        assert catalogo.sku == "ma1gela"
        assert catalogo.name == "geladeira"
        assert isinstance(catalogo.seller_id, str)
        assert isinstance(catalogo.created_at, datetime)
        assert catalogo.updated_at is None



    def test_update_catalogo(self):
        """Testa a atualização dos campos de uma instância de Price."""
        catalogo = CatalogoModel(seller_id="magalu1", sku="ma1gela", name="geladeira")

        # Atualiza os campos de preço
        catalogo.name = "geladeira nova"

        assert catalogo.name == "geladeira nova"

        #assert preco.seller_id == "1"  # Não alterado
        #assert preco.sku == "A"  # Não alterado

    def test_from_json(self):
        """Testa a criação de uma instância de Price a partir de um JSON."""
        json_data = '{"seller_id": "magalu22", "sku": "ma22gela", "name": "geladeira22"}'
        catalogo = CatalogoModel.from_json(json_data)

        assert catalogo.seller_id == "magalu22"
        assert catalogo.sku == "ma22gela"
        assert catalogo.name == "geladeira22"
        assert isinstance(catalogo.seller_id,str)

    def test_create_catalogo_with_missing_fields_raises_error(self):
        """Testa se a criação de CatalogoModel sem campos obrigatórios levanta erro."""
        # seller_id ausente
        with pytest.raises(ValidationError):
            CatalogoModel(sku="A", name="Produto")
        # sku ausente
        with pytest.raises(ValidationError):
            CatalogoModel(seller_id="1", name="Produto")
        # name ausente
        with pytest.raises(ValidationError):
            CatalogoModel(seller_id="1", sku="A")

    def test_create_catalogo_with_short_name_raises_error(self):
        """Testa se a criação de CatalogoModel com name de 1 caractere levanta erro."""
        with pytest.raises(ValidationError):
            CatalogoModel(seller_id="magalu1", sku="ma1-gela", name="a")


