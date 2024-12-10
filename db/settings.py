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


class SettingsMongo(BaseSettings):
    MONGO_INITDB_ROOT_DATABASE: str
    MONGO_INITDB_ROOT_USERNAME: SecretStr
    MONGO_INITDB_ROOT_PASSWORD: SecretStr
    MONGO_INITDB_ROOT_HOST: str
    MONGO_INITDB_ROOT_PORT: int

    @property
    def MONGODB_URL(self) -> str:
        return (
            f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME.get_secret_value()}"
            f":{self.MONGO_INITDB_ROOT_PASSWORD.get_secret_value()}"
            f"@{self.MONGO_INITDB_ROOT_HOST}:{self.MONGO_INITDB_ROOT_PORT}/{self.MONGO_INITDB_ROOT_DATABASE}")

    @property
    def MONGODB_MOTOR_URL(self) -> str:
        return (
            f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME.get_secret_value()}"
            f":{self.MONGO_INITDB_ROOT_PASSWORD.get_secret_value()}"
            f"@{self.MONGO_INITDB_ROOT_HOST}:{self.MONGO_INITDB_ROOT_PORT}")

    model_config = SettingsConfigDict(env_file="db/mongo/.mongo.env")


class SettingsInflux(BaseSettings):
    DOCKER_INFLUXDB_INIT_ORG: str
    INFLUX_HOST: str
    INFLUX_PORT: int
    TOKEN: SecretStr

    @property
    def INFLUX_CLIENT_URL(self) -> str:
        return f"http://{self.INFLUX_HOST}:{self.INFLUX_PORT}"

    model_config = SettingsConfigDict(env_file="db/influxdb2/.influxdb2.env", extra="allow")


class SettingsCH(BaseSettings):
    CLICKHOUSE_DB: str
    CLICKHOUSE_USER: SecretStr
    CLICKHOUSE_PASSWORD: SecretStr
    CLICKHOUSE_HOST: str
    CLICKHOUSE_PORT: int

    @property
    def CLICKHOUSE_ASYNC_URL(self) -> str:
        return (f"clickhouse+asynch://{self.CLICKHOUSE_USER.get_secret_value()}"
                f":{self.CLICKHOUSE_PASSWORD.get_secret_value()}"
                f"@{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}/{self.CLICKHOUSE_DB}")

    @property
    def CLICKHOUSE_NATIVE_URL(self) -> str:
        return (f"clickhouse+native://{self.CLICKHOUSE_USER.get_secret_value()}"
                f":{self.CLICKHOUSE_PASSWORD.get_secret_value()}"
                f"@{self.CLICKHOUSE_HOST}:{self.CLICKHOUSE_PORT}/{self.CLICKHOUSE_DB}")

    model_config = SettingsConfigDict(env_file="db/clickhouse/.clickhouse.env")


class SettingsRuntime(BaseSettings):
    BATCH_SIZE: int = 5_000
