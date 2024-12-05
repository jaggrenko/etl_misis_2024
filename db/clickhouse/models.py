from clickhouse_sqlalchemy import get_declarative_base, types, engines
from sqlalchemy import Column, MetaData, create_engine, func

from settings import SettingsCH

settings = SettingsCH()

engine = create_engine(settings.CLICKHOUSE_URL)
metadata = MetaData()
metadata.create_all(bind=engine)

Base = get_declarative_base(metadata=metadata)


class DescriptionGraduatesUniversity(Base):
    id = Column(types.Int8, primary_key=True)
    year = Column(types.Date, nullable=False)
    average_salary = Column(types.Float, nullable=True)
    percent_employed = Column(types.Float, nullable=False)
    grouping = Column(types.Int32, nullable=False)

    __table_args__ = (
        engines.CollapsingMergeTree(id, partition_by=func.toYYYYMM(year), order_by=(year, average_salary)),
    )


class DD(Base):
    id = Column(types.Int8, primary_key=True)
    year = Column(types.Date, nullable=False)
    average_salary = Column(types.Float, nullable=True)
    percent_employed = Column(types.Float, nullable=False)
    grouping = Column(types.Int32, nullable=False)