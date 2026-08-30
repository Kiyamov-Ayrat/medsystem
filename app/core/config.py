from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # App
    app_env: str = "development"
    app_debug: bool = False
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30

    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    #
    # @property
    # def database_url(self) -> str:
    #
    #     return (
    #         f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
    #         f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    #     )