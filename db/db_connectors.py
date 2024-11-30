import logging
from abc import ABC, abstractmethod
from enum import Enum
from contextlib import contextmanager
from typing import AsyncContextManager, TypeVar, Type

import psycopg2
from backoff import expo, on_exception
from pymongo import MongoClient, errors as mongo_errors

logger = logging.getLogger(__name__)


class ConnectorType(Enum):
    Postgres = "Postgres"
    MongoDB = "MongoDB"


T = TypeVar("T", bound=AsyncContextManager)


class _DBConnectorAbstract(ABC):
    """Parent for any connector-classes"""

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Method not implemented!")


class _PostgresConnector(_DBConnectorAbstract):
    """Postgres connector-class yields"""

    @contextmanager
    @on_exception(
        expo,
        psycopg2.Error,
        logger=logger,
        max_tries=10
    )
    def __call__(self, **dsn: str) -> T:

        try:
            _connection = psycopg2.connect(**dsn)
            yield _connection
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as err:
            logger.error(
                "Postgres error occurred: {0} {1}"
                .format(err, self.__class__.__name__)
            )

        # _connection.close()


class _MongoConnector(_DBConnectorAbstract):
    """MongoDB connector-class yields"""

    @contextmanager
    @on_exception(
        expo,
        mongo_errors.ConnectionFailure,
        logger=logger
    )
    def __call__(self, host: str, port: int, username: str, password: str) -> T:
        try:
            _connection = MongoClient(host,
                                      port,
                                      username=username,
                                      password=password)

            yield _connection
        except mongo_errors.ConnectionFailure as err:
            logger.error(
                "Mongo error occurred: {0} {1}"
                .format(err, self.__class__.__name__)
            )


class ConnectionFactory:
    CONNECTIONS = {
        ConnectorType.Postgres: _PostgresConnector,
        ConnectorType.MongoDB: _MongoConnector,
    }

    @classmethod
    def connect_db(cls, connector_type: ConnectorType) -> Type[
        _PostgresConnector | _MongoConnector | None
    ]:
        connector = cls.CONNECTIONS.get(connector_type)

        return connector()
