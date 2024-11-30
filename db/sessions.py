from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import Settings

settings = Settings()

engine = create_async_engine(settings.POSTGRES_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
