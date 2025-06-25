import pytest


@pytest.fixture
def mock_do_auth(app_v2):
    """
    Mocando o do_auth para o app_v2 usado nos testes
    """
    from app.api.common.auth_handler import do_auth

    app_v2.dependency_overrides[do_auth] = lambda: None
    yield
    app_v2.dependency_overrides.pop(do_auth, None)