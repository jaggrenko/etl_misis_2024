import motor.motor_asyncio as motor_asyncio

from settings import SettingsMongo

settings = SettingsMongo()

mongo_async_client = motor_asyncio.AsyncIOMotorClient(settings.MONGODB_MOTOR_URL)
