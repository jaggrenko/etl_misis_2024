from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.settings import SettingsCH, SettingsMongo, SettingsPG

settings = SettingsPG()

engine_pg = create_async_engine(settings.POSTGRES_URL, poolclass=NullPool)
pg_async_session_maker = async_sessionmaker(engine_pg, expire_on_commit=False)

settings = SettingsMongo()

engine_mongo = create_engine(settings.MONGODB_URL, poolclass=NullPool)
mongo_sync_session_maker = sessionmaker(engine_mongo, expire_on_commit=False)

settings = SettingsCH()

engine_ch = create_async_engine(settings.CLICKHOUSE_ASYNC_URL, poolclass=NullPool)
ch_async_session_maker = async_sessionmaker(engine_ch, expire_on_commit=False)
