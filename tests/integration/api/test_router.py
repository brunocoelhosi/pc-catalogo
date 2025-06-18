from app.api import router as api_router


def test_router_configuracoes_existem():
    configuracoes = api_router.router_configurations
    assert isinstance(configuracoes, list)
    assert len(configuracoes) == 2
    assert all(len(cfg) >= 2 for cfg in configuracoes)
    assert any("/seller/v1" in cfg[1] for cfg in configuracoes)
    assert any("/seller/v2" in cfg[1] for cfg in configuracoes)
