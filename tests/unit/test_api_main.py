import pytest
from fastapi import FastAPI
import importlib

def test_api_main(): 

    # Import the app module dynamically
    app_module = importlib.import_module("app.api_main")
    
    # Inicializa o fastapi
    app: FastAPI = app_module.init()

    assert isinstance(app, FastAPI)
    
    # Verifica se o app tem rotas registradas
    assert len(app.routes) > 0  