from pydantic import Field
from pydantic_settings import BaseSettings

from constants import ENV_PATH


class _SettingsBase(BaseSettings):
    """Base settings."""

    class Config:
        """Config for the meta class in current settings."""

        env_file = ENV_PATH
        extra = "ignore"


class SettingsDatabase(_SettingsBase):
    """Settings Database."""

    db: str = Field(alias="DB")
    user: str = Field(alias="DB_USER")
    password: str = Field(alias="DB_PASSWORD")
    host: str = Field(alias="DB_SERVER")
    port: str = Field(alias="DB_PORT")

    @property
    def database_url(self) -> str:
        """Return database url from .env ."""
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db,
        )


class SettingsTestDatabase(_SettingsBase):
    """Settings for test database."""

    db: str = Field(alias="TEST_DB")
    user: str = Field(alias="TEST_DB_USER")
    password: str = Field(alias="TEST_DB_PASSWORD")
    host: str = Field(alias="TEST_DB_SERVER")
    port: str = Field(alias="TEST_DB_PORT")

    @property
    def database_url(self) -> str:
        """Return database url from .env ."""
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.db,
        )


database_config = SettingsDatabase()
test_database_config = SettingsTestDatabase()
