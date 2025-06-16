from fastapi import FastAPI

from app.api.api_application import create_app
from app.api.router import routes
from app.settings import api_settings


def test_criacao_app_fastapi():
    app = create_app(api_settings, routes)
    assert isinstance(app, FastAPI)
    assert getattr(app, "title", None) == api_settings.app_name
    openapi_schema = getattr(app, "openapi_schema", None) or app.openapi()
    assert openapi_schema["openapi"] == "3.0.2"
    assert getattr(app, "version", None) == api_settings.version


def test_rotas_incluidas():
    app = create_app(api_settings, routes)
    urls = [getattr(route, "path", None) for route in getattr(app, "routes", [])]
    # Verifica se as rotas principais estão presentes
    #assert any("/api/v1" in str(url) for url in urls)
    assert any("/seller/v2/catalogo" in str(url) for url in urls)
