from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)


class DescriptionGraduatesUniversity(BaseModel):
    __tablename__ = 'data_graduates'

    object_level = Column(String(6))
    object_name = Column(String(64))
    gender = Column(String(7))
    education_level = Column(String(64))
    year = Column(Integer)
    university = Column(String(256))
    special_section = Column(String(256))
    speciality = Column(String(256))
    speciality_code = Column(String(8))
    count_graduate = Column(Integer)
    percent_employed = Column(Float)
    average_salary = Column(Float)
    oktmo = Column(String(14))
    okato = Column(String(9))
