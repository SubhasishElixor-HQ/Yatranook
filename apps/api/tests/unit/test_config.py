import pytest

from app.core.config import Settings


def production_settings(**overrides) -> Settings:
    values = {
        "app_env": "production",
        "database_url": "postgresql+psycopg://yatranook:" + ("a" * 48) + "@localhost:5432/yatranook",
        "jwt_secret": "b" * 64,
        "allowed_hosts": "127.0.0.1,localhost,yatranook.example.com",
        "cors_origins": "https://yatranook.example.com",
    }
    values.update(overrides)
    return Settings(**values)


def test_valid_production_settings_are_accepted() -> None:
    production_settings().validate_production_secrets()


def test_development_jwt_secret_is_rejected_in_production() -> None:
    settings = production_settings(jwt_secret="dev-only-change-this-secret-000000000000")
    with pytest.raises(RuntimeError, match="JWT_SECRET"):
        settings.validate_production_secrets()


def test_short_database_password_is_rejected_in_production() -> None:
    settings = production_settings(database_url="postgresql+psycopg://user:short@localhost:5432/db")
    with pytest.raises(RuntimeError, match="PostgreSQL password"):
        settings.validate_production_secrets()


def test_wildcard_host_is_rejected_in_production() -> None:
    settings = production_settings(allowed_hosts="*")
    with pytest.raises(RuntimeError, match="ALLOWED_HOSTS"):
        settings.validate_production_secrets()
