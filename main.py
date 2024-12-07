import asyncio
from bson.objectid import ObjectId
import datetime

from db.dao import MongoAsyncDAO, MongoSyncDAO, PostgresAsyncDAO
from db.mongo.models import DataGraduates
from db.postgres.models import DescriptionGraduatesUniversity as DGU_db_model
from etl.models import DescriptionGraduatesUniversity as DGU_data_model
from settings import SettingsRuntime

runtime_settings = SettingsRuntime()


class DescriptionGraduatesUniversityDAO(PostgresAsyncDAO):
    model = DGU_db_model


class AggregatedDataSyncDAO(MongoSyncDAO):
    model = DataGraduates


class AggregatedDataAsyncDAO(MongoAsyncDAO):
    database = "test"
    collection = "data_graduates"


async def main():
    start_time = datetime.datetime.now()
    records = DescriptionGraduatesUniversityDAO.fetch_all_batch()

    records_counter: int = 0
    mongo_records: list = []

    async for record in records:
        record = DGU_data_model(**record)
        record = record.model_dump(exclude={"id"})
        mongo_records.append(record)
        records_counter += 1
        if records_counter == runtime_settings.BATCH_SIZE:
            await AggregatedDataAsyncDAO.insert_many(mongo_records)
            records_counter = 0
            mongo_records = []
    else:
        await AggregatedDataAsyncDAO.insert_many(mongo_records)

    print(datetime.datetime.now() - start_time)


if __name__ == '__main__':
    asyncio.run(main())
