import asyncio
from bson.objectid import ObjectId
import datetime

from db.dao import MongoAsyncDAO, MongoSyncDAO, PostgresAsyncDAO
from db.mongo.models import DataGraduates
from db.postgres.models import DescriptionGraduatesUniversity as DGU_db_model
from etl.models import DescriptionGraduatesUniversity as DGU_data_model


# from db.db_connectors import ConnectionFactory, ConnectorType
#
# pg_connector = ConnectionFactory.connect_db(ConnectorType.Postgres)
#
# dsn = {
#     'user': 'postgres',
#     'password': 'postgres',
#     'dbname': 'postgres',
#     'host': 'localhost',
#     'port': 5432,
# }


class DescriptionGraduatesUniversityDAO(PostgresAsyncDAO):
    model = DGU_db_model


class AggregatedDataSyncDAO(MongoSyncDAO):
    model = DataGraduates


class AggregatedDataAsyncDAO(MongoAsyncDAO):
    database = "test"
    collection = "data_graduates"


# connection = pg_connector('postgresql://postgres:postgres@localhost:5432/postgres')
# connection = pg_connector(**dsn)

async def main():
    records = await DescriptionGraduatesUniversityDAO.fetch_one(**{"id": 1})
    data_model = DGU_data_model(**records)
    print(data_model.university, data_model.id)

    # records = await DescriptionGraduatesUniversityDAO.fetch_all()
    # for record in records:
    #     print(DGU_data_model(**record))

    start_time = datetime.datetime.now()
    records = DescriptionGraduatesUniversityDAO.fetch_all_batch()

    records_counter: int = 0
    mongo_records: list = []

    BATCH_SIZE = 1_000

    async for record in records:
        record = DGU_data_model(**record)
        record = record.model_dump(exclude={"id"})
        record["_id"] = ObjectId()
        await asyncio.sleep(0.01)
        mongo_records.append(record)
        records_counter += 1
        if records_counter == BATCH_SIZE:
            await AggregatedDataAsyncDAO.insert_many(mongo_records)
            records_counter = 0
            # await asyncio.sleep(0.1)

        # print(DGU_data_model(**record).model_dump(exclude={"id"}))
    print(datetime.datetime.now() - start_time)

    # zz = await AggregatedDataAsyncDAO.fetch_one(**{"name": "lesson is boring"})
    # bb = await AggregatedDataAsyncDAO.insert_one({"name": "lesson is awful boring"})

    # print(bb)


if __name__ == '__main__':
    asyncio.run(main())
