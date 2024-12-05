from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsPG(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER.get_secret_value()}:{self.POSTGRES_PASSWORD.get_secret_value()}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    model_config = SettingsConfigDict(env_file="db/postgres/.postgres.env")


class SettingsCH(BaseSettings):
    CLICKHOUSE_DB: str
    CLICKHOUSE_USER: SecretStr
    CLICKHOUSE_PASSWORD: SecretStr
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int

    @property
    def CLICKHOUSE_URL(self) -> str:
        return (
            f"clickhouse+native://{self.CLICKHOUSE_USER.get_secret_value()}:{self.CLICKHOUSE_PASSWORD.get_secret_value()}"
            f"@{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}/{self.CLICKHOUSE_DB}")

    model_config = SettingsConfigDict(env_file="db/clickhouse/.clickhouse.env")


class SettingsInflux(BaseSettings):
    INFLUXDB_DB: str
    INFLUXDB_USER: SecretStr
    INFLUXDB_PASSWORD: SecretStr
    INFLUXDB_HOST: str
    INFLUXDB_PORT: int

    @property
    def INFLUXDB_URL(self) -> str:
        return (
            f"flightsql://{self.INFLUXDB_HOST}:{self.INFLUXDB_PORT}"
        )

    # f"{self.INFLUXDB_USER.get_secret_value()}:{self.INFLUXDB_PASSWORD.get_secret_value()}"
    # f"@{self.INFLUXDB_HOST}:{self.INFLUXDB_PORT}/{self.INFLUXDB_DB}")

    model_config = SettingsConfigDict(env_file="db/influxdb2/.influxdb.env")


class SettingsMongo(BaseSettings):
    MONGO_DB: str
    MONGO_USER: SecretStr
    MONGO_PASSWORD: SecretStr
    MONGO_HOST: str
    MONGO_PORT: int

    @property
    def MONGO_URL(self) -> str:
        return (
            f"mongodb://{self.MONGO_USER.get_secret_value()}:{self.MONGO_PASSWORD.get_secret_value()}"
            f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB}")

    model_config = SettingsConfigDict(env_file="db/mongo/.mongo.env")
