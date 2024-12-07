from abc import ABC, abstractmethod
from typing import AsyncGenerator, Iterable, TypeVar  # TODO: Mapping?

from sqlalchemy import select

from connectors import mongo_async_client
from db.sessions import mongo_sync_session_maker, pg_async_session_maker

BATCH_SIZE = 10_000
METHOD_NOT_IMPLEMENTED = "This abstract method must be implemented."

record = TypeVar("record")
ObjectID = TypeVar("ObjectID")


class AbstractDAO(ABC):
    @classmethod
    @abstractmethod
    async def fetch_one(cls, *args, **kwargs):
        raise NotImplementedError(METHOD_NOT_IMPLEMENTED)

    @classmethod
    @abstractmethod
    async def fetch_all(cls, *args, **kwargs):
        raise NotImplementedError(METHOD_NOT_IMPLEMENTED)

    @classmethod
    @abstractmethod
    async def fetch_all_batch(cls, *args, **kwargs):
        raise NotImplementedError(METHOD_NOT_IMPLEMENTED)

    @classmethod
    @abstractmethod
    async def insert_one(cls, *args, **kwargs):
        raise NotImplementedError(METHOD_NOT_IMPLEMENTED)

    @classmethod
    @abstractmethod
    async def insert_many(cls, *args, **kwargs):
        raise NotImplementedError(METHOD_NOT_IMPLEMENTED)


class PostgresAsyncDAO(AbstractDAO):
    model = None

    @classmethod
    async def fetch_one(cls, **filters):
        async with pg_async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(stmt)

            return result.mappings().one_or_none()

    @classmethod
    async def fetch_all(cls, **filters):
        async with pg_async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(stmt)

            return result.mappings().all()

    @classmethod
    async def fetch_all_batch(cls, batch_size=BATCH_SIZE, **filters) -> AsyncGenerator:
        async with pg_async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.stream(stmt.execution_options(yield_per=batch_size))

            async for record in result:
                yield record._asdict()

    @classmethod
    async def insert_one(cls, *args, **kwargs):
        pass

    @classmethod
    async def insert_many(cls, *args, **kwargs):
        pass


class MongoSyncDAO(AbstractDAO):
    model = None

    @classmethod
    def fetch_one(cls, *args, **kwargs):
        pass

    @classmethod
    def fetch_all(cls, *args, **kwargs):
        pass

    @classmethod
    def fetch_all_batch(cls, *args, **kwargs):
        pass

    @classmethod
    def insert_one(cls, instance: record):
        with mongo_sync_session_maker() as session:
            session.add(cls.model(**instance))
            session.commit()

    @classmethod
    def insert_many(cls, instances: Iterable):
        with mongo_sync_session_maker() as session:
            session.add_all(cls.model(**instance) for instance in instances)
            session.commit()


class MongoAsyncDAO(AbstractDAO):
    database: str = None
    collection: str = None

    @classmethod
    async def fetch_one(cls, **filter_by):
        db = mongo_async_client[cls.database]
        collection = db[cls.collection]

        return await collection.find_one({**filter_by})

    @classmethod
    async def fetch_all(cls, *args, **kwargs):
        pass

    @classmethod
    async def fetch_all_batch(cls, *args, **kwargs):
        pass

    @classmethod
    async def insert_one(cls, record: dict) -> ObjectID:
        db = mongo_async_client[cls.database]
        collection = db[cls.collection]

        return await collection.insert_one(record)

    @classmethod
    async def insert_many(cls, records: Iterable[dict]):
        db = mongo_async_client[cls.database]
        collection = db[cls.collection]

        return await collection.insert_many(records)
