import asyncio
import datetime

from db.dao import ClickhouseAsyncDAO, InfluxAsyncDAO, MongoAsyncDAO, MongoSyncDAO, PostgresAsyncDAO
from db.clickhouse.models import DescriptionGraduatesUniversity as DGU_db_ch_model
from db.mongo.models import DescriptionGraduatesUniversity as DGU_db_mg_model
from db.postgres.models import DescriptionGraduatesUniversity as DGU_db_pg_model
from db.settings import SettingsRuntime
from rmq.publisher import publish
from transform.DTO import InterfaceDTO
from transform.models import DescriptionGraduatesUniversity as DGU_data_model


runtime_settings = SettingsRuntime()


class PostgresDBAsyncDAO(PostgresAsyncDAO):
    model = DGU_db_pg_model


class MongoDBSyncDAO(MongoSyncDAO):
    model = DGU_db_mg_model


class MongoDBAsyncDAO(MongoAsyncDAO):
    database = "test"
    collection = "data_graduates"


class InfluxDBAsyncDAO(InfluxAsyncDAO):
    bucket = "data_graduates"


class ClickhouseDBAsyncDAO(ClickhouseAsyncDAO):
    model = DGU_db_ch_model


interface_dto = InterfaceDTO()


async def load(loop, record):
    mongo, influx, clickhouse = interface_dto.get_transformed()

    await MongoDBAsyncDAO.insert_many(mongo)
    await InfluxDBAsyncDAO.insert_many(influx)
    await ClickhouseDBAsyncDAO.insert_many(clickhouse)

    await publish(loop, record)

    interface_dto.clear()


async def main():
    start_time = datetime.datetime.now()
    records = PostgresDBAsyncDAO.fetch_all_batch()

    records_counter: int = 0
    total_records_counter: int = 0
    # mongo_records: list = []
    # influx_records: list = []
    # clickhouse_records: list = []

    async for record in records:
        record = DGU_data_model(**record)
        interface_dto.transform(record)
        #
        # mongo_records.append(record.model_dump(exclude={"id"}))
        #
        # measurement: dict = {"measurement": "data_graduates", "fields": record.model_dump(exclude={"id"}), }
        # influx_records.append(measurement)
        #
        # years: str = str(record.year)
        # years: datetime.date = datetime.datetime.strptime(years, "%Y")
        # clickhouse_record = record.model_dump(include={"average_salary", "percent_employed", "id"}, )
        #
        # clickhouse_record["years"] = years
        # clickhouse_record["Sign"] = 1
        # clickhouse_records.append(clickhouse_record)

        records_counter += 1
        total_records_counter += 1
        if records_counter == runtime_settings.BATCH_SIZE:
            await load(loop, record)
            # await MongoDBAsyncDAO.insert_many(mongo_records)
            # await InfluxDBAsyncDAO.insert_many(influx_records)
            # await ClickhouseDBAsyncDAO.insert_many(clickhouse_records)

            records_counter = 0
            # mongo_records, influx_records, clickhouse_records = [], [], []
    else:
        await load(loop, record)
        # await MongoDBAsyncDAO.insert_many(mongo_records)
        # await InfluxDBAsyncDAO.insert_many(influx_records)
        # await ClickhouseDBAsyncDAO.insert_many(clickhouse_records)

    print(datetime.datetime.now() - start_time)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    #asyncio.run(main())
