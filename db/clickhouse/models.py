from clickhouse_sqlalchemy import get_declarative_base, types, engines
from sqlalchemy import Column, MetaData, create_engine, func

from db.settings import SettingsCH

settings = SettingsCH()

engine = create_engine(settings.CLICKHOUSE_NATIVE_URL)
metadata = MetaData()
metadata.create_all(bind=engine)

Base = get_declarative_base(metadata=metadata)


class DescriptionGraduatesUniversity(Base):
    Sign = Column(types.Int8, nullable=False)
    average_salary = Column(types.Float, nullable=True)
    id = Column(types.Int8, primary_key=True)
    percent_employed = Column(types.Float, nullable=False)
    grouping = Column(types.Int32, nullable=False)
    years = Column(types.Date, nullable=False)

    __table_args__ = (
        engines.CollapsingMergeTree(id, partition_by=func.toYYYYMM(years), order_by=(years, average_salary)),
    )
