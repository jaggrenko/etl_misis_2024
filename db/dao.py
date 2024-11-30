from abc import ABC, abstractmethod
from typing import AsyncGenerator

from sqlalchemy import select

from db.sessions import async_session_maker


BATCH_SIZE = 10_000
METHOD_NOT_IMPLEMENTED = "This abstract method must be implemented."


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


class PostgresDAO(AbstractDAO):
    model = None

    @classmethod
    async def fetch_one(cls, **filters):
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(stmt)

            return result.mappings().one_or_none()

    @classmethod
    async def fetch_all(cls, **filters):
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.execute(stmt)

            return result.mappings().all()

    @classmethod
    async def fetch_all_batch(cls, batch_size=BATCH_SIZE, **filters) -> AsyncGenerator:
        async with async_session_maker() as session:
            stmt = select(cls.model.__table__.columns).filter_by(**filters)
            result = await session.stream(stmt.execution_options(yield_per=batch_size))

            async for record in result:
                yield record._asdict()
