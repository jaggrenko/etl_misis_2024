from abc import ABC, abstractmethod
from enum import Enum
from typing import Generator

from db.db_connectors import ConnectionFactory


#from DB.utils.db_connectors import ConnectionFactory, ConnectorType


# from db_connectors import ConnectionFactory
class MongoRequestType(Enum):
    InsertOne = "InsertOne"
    FindOne = "GetOne"


class _DBHandlerAbstract(ABC):
    """Parent for any db_handler-classes"""


class _AnyDBHandler(_DBHandlerAbstract):
    """Init class for any db_handler-class"""

    def __init__(self, connector: ConnectionFactory):
        self.connector = connector

    @abstractmethod
    def db_handle(self, *args, **kwargs):
        pass


class _SQLiteRead:
    """SQLite read data query"""

    def _execute_sql(self, db_path: str, query: str) -> Generator:
        with self.connector(db_path) as connection:
            cursor = connection.cursor()
            query_result = cursor.execute(query)

        yield from query_result


class SQLiteHandler(_AnyDBHandler, _SQLiteRead):
    """Run SQLite queries"""

    def db_handle(self, db_name: str, query: str, *args, ):
        query_result = self._execute_sql(db_name, query)

        for result in query_result:
            yield result
            # print(*result,)


# class _MongoReadOne:
#     """Mongo read document query"""
#
#     def _execute_sql(self,
#                      host: str,
#                      port: int,
#                      username: str,
#                      password: str,
#                      db_name: str,
#                      collection: str,
#                      element: dict) -> Generator:
#         with self.connector(host, port, username, password) as connection:
#             db = connection[db_name]
#             collection = db[collection]
#
#             query_result = collection.find(element)
#
#         yield from query_result
#
#
# class _MongoInsertOne:
#     """Mongo insert document query"""
#
#     def _execute_sql(self,
#                      host: str,
#                      port: int,
#                      username: str,
#                      password: str,
#                      db_name: str,
#                      collection: str,
#                      element: dict) -> Generator:
#         with self.connector(host, port, username, password) as connection:
#             db = connection[db_name]
#             collection = db[collection]
#
#             query_result = collection.insert_one(element).inserted_id
#
#         yield from query_result


class _GetMongoCollection:
    """Returns gen of Mongo collection"""

    def _get_collection(self,
                        host: str,
                        port: int,
                        username: str,
                        password: str,
                        db_name: str,
                        collection: str) -> Generator:
        with self.connector(host, port, username, password) as connection:
            db = connection[db_name]
            collection = db[collection]

            return collection


class MongoHandler(_AnyDBHandler, _GetMongoCollection):  # _MongoReadOne):
    """Run Mongo queries"""

    def db_handle(self,
                  host: str,
                  port: int,
                  username: str,
                  password: str,
                  db_name: str,
                  collection: str,
                  element: dict,
                  action: MongoRequestType,
                  *args, ):
        mongo_collection = self._get_collection(
            host,
            port,
            username,
            password,
            db_name,
            collection)

        ACTIONS = {
            MongoRequestType.FindOne: mongo_collection.find,
            MongoRequestType.InsertOne: mongo_collection.insert_one,
        }

        query_result = ACTIONS.get(action)

        yield query_result(element)


# connector = ConnectionFactory.connect_db(ConnectorType.MongoDB)
#
# mongo = MongoHandler(connector)
# spam = mongo.db_handle("localhost",
#                        27017,
#                        "mongodb",
#                        "mongodb",
#                        "test",
#                        "sales_aggregated_data",
#                        {"name": "Grace of Docker II"},
#                        MongoRequestType.InsertOne
#                        )
#
# print(type(spam))
#
# for ham in spam:
#     print(ham)

# connector = ConnectionFactory.connect_db(ConnectorType.SQLite)
#
# sql = SQLiteHandler(connector)
# sql.db_handle("../../bicycles_db", select_all("adventureworksproducts"))
