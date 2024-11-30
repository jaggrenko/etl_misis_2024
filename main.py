import asyncio
import datetime

from db.dao import PostgresDAO
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


class DescriptionGraduatesUniversityDAO(PostgresDAO):
    model = DGU_db_model


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
    async for record in records:
        print(DGU_data_model(**record))
    print(datetime.datetime.now() - start_time)


if __name__ == '__main__':
    asyncio.run(main())
