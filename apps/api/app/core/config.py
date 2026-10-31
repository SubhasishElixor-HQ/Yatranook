from functools import lru_cache

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../../.env"), extra="ignore", case_sensitive=False)

    app_name: str = "Yatranook API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://yatranook:yatranook_dev_only@localhost:5432/yatranook"
    jwt_secret: SecretStr = SecretStr("dev-only-change-this-secret-before-deployment-000000000000")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = Field(default=30, ge=5, le=1440)
    cors_origins: str = "http://localhost:5173,http://localhost:8080"
    allowed_hosts: str = "localhost,127.0.0.1"
    ollama_base_url: str = "http://host.docker.internal:11434"
    ollama_chat_model: str = "qwen2.5-coder:3b"
    ollama_embedding_model: str = "nomic-embed-text"
    embedding_dimensions: int = 1536
    osrm_base_url: str | None = None
    log_level: str = "INFO"

    @model_validator(mode="after")
    def validate_embedding_dimension(self):
        if self.embedding_dimensions != 1536:
            raise ValueError("The initial pgvector migration uses Vector(1536); keep EMBEDDING_DIMENSIONS=1536")
        return self

    @field_validator("app_env")
    @classmethod
    def normalize_env(cls, value: str) -> str:
        return value.lower().strip()

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def allowed_host_list(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    def validate_production_secrets(self) -> None:
        if not self.is_production:
            return

        secret = self.jwt_secret.get_secret_value()
        if len(secret) < 32 or secret.startswith("dev-only"):
            raise RuntimeError("JWT_SECRET must be a unique secret of at least 32 characters in production")

        try:
            database_password = make_url(self.database_url).password or ""
        except Exception as exc:
            raise RuntimeError("DATABASE_URL must be a valid PostgreSQL connection URL") from exc
        if len(database_password) < 24 or database_password == "local-development-only":
            raise RuntimeError("Use a unique URL-safe PostgreSQL password of at least 24 characters in production")

        hosts = self.allowed_host_list
        if not hosts or "*" in hosts or set(hosts).issubset({"localhost", "127.0.0.1"}):
            raise RuntimeError("ALLOWED_HOSTS must include the real production hostname and must not use a wildcard")
        if "*" in self.cors_origin_list:
            raise RuntimeError("CORS_ORIGINS must not use a wildcard in production")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_production_secrets()
    return settings


settings = get_settings()
