import pytest
import sys
import importlib

def test_environment_enum_properties(monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    from app.settings.base import EnvironmentEnum
    assert EnvironmentEnum.DEVELOPMENT.is_development
    assert not EnvironmentEnum.DEVELOPMENT.is_test
    assert not EnvironmentEnum.DEVELOPMENT.is_production

    assert EnvironmentEnum.TEST.is_test
    assert not EnvironmentEnum.TEST.is_development
    assert not EnvironmentEnum.TEST.is_production

    assert EnvironmentEnum.PRODUCTION.is_production
    assert not EnvironmentEnum.PRODUCTION.is_development
    assert not EnvironmentEnum.PRODUCTION.is_test

def test_env_files_mapping(monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    from app.settings.base import ENV_FILES
    assert ENV_FILES["dev"] == "dotenv.dev"
    assert ENV_FILES["prod"] == "dotenv.prod"
    assert ENV_FILES["test"] == "dotenv.test"

def test_base_settings_defaults(monkeypatch):
    monkeypatch.setenv("ENV", "dev")
    from app.settings.base import BaseSettings, EnvironmentEnum
    settings = BaseSettings()
    assert settings.env == EnvironmentEnum.DEVELOPMENT
    assert settings.env_file.endswith("dotenv.dev")

def test_base_settings_env_test(monkeypatch):
    monkeypatch.setenv("ENV", "test")
    if "app.settings.base" in sys.modules:
        del sys.modules["app.settings.base"]
    from app.settings.base import BaseSettings
    settings = BaseSettings()
    assert "dotenv.test" in settings.env_file

def test_invalid_env(monkeypatch):
    monkeypatch.setenv("ENV", "invalid")
    if "app.settings.base" in sys.modules:
        del sys.modules["app.settings.base"]
    with pytest.raises(ValueError, match="ENV must be either 'dev', 'prod' or 'test'"):
        importlib.import_module("app.settings.base")