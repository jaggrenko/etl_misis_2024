import motor.motor_asyncio as motor_asyncio

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from db.settings import SettingsMongo, SettingsInflux

settings_mongo = SettingsMongo()
settings_influx = SettingsInflux()

mongo_async_client = motor_asyncio.AsyncIOMotorClient(settings_mongo.MONGODB_MOTOR_URL)


def influx_async_client():
    return InfluxDBClientAsync(settings_influx.INFLUX_CLIENT_URL, settings_influx.TOKEN.get_secret_value(),
                               settings_influx.DOCKER_INFLUXDB_INIT_ORG, connection_pool_maxsize=10)
