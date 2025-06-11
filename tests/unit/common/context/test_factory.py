import pytest
from app.common.context.factory import set_context, get_context, _app_context
from app.common.context.model import AppContext
from app.common.exceptions import ForbiddenException

def test_set_and_get_context():
    ctx = AppContext()
    set_context(ctx)
    assert get_context() is ctx

def test_get_context_without_set(monkeypatch):
    # Garante que o contexto está limpo
    token = _app_context.set(None)
    with pytest.raises(ForbiddenException):
        get_context()
    _app_context.reset(token)