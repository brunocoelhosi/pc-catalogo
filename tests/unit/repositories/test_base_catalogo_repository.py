from app.repositories.catalogo_repository import CatalogoRepository
from app.models.catalogo_model import CatalogoModel
from app.integrations.database.mongo_client import MongoClient

def test_catalogo_repository_init():
    client = MongoClient("mongodb://admin:admin@localhost:27018/test_db?authSource=admin")
    repo = CatalogoRepository(client)
    assert repo.COLLECTION_NAME == "catalogo"
    assert repo.model_class == CatalogoModel
    client.close()