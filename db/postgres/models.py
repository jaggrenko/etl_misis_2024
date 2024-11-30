from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class DescriptionGraduatesUniversity(BaseModel):
    __tablename__ = 'description_graduates_university'

    object_level = Column(String(6), nullable=False)
    object_name = Column(String(64), nullable=False)
    gender = Column(String(7), nullable=False)
    education_level = Column(String(64), nullable=False)
    year = Column(Integer, nullable=False)
    university = Column(String(256), nullable=False)
    special_section = Column(String(256), nullable=False)
    speciality = Column(String(256), nullable=False)
    speciality_code = Column(String(8), nullable=False)
    count_graduate = Column(Integer, nullable=False)
    percent_employed = Column(Float, nullable=False)
    average_salary = Column(Float, nullable=True)
    oktmo = Column(String(14), nullable=False)
    okato = Column(String(9), nullable=False)
