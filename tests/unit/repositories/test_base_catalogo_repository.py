from app.repositories.catalogo_repository import CatalogoRepository
from app.models.catalogo_model import CatalogoModel
from unittest.mock import MagicMock


def test_catalogo_repository_init():
    client = MagicMock()  # ou use um mock adequado do seu mongo client
    repo = CatalogoRepository(client)
    assert repo.collection_name == "catalogo"
    assert repo.model_class == CatalogoModel