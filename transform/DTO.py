from abc import ABC, abstractmethod
from datetime import datetime
from typing import Generator, NoReturn

from pydantic import BaseModel

METHOD_NOT_IMPLEMENTED = "This abstract method must be implemented."


class AbstractDTO(ABC):
    def __init__(self):
        self.accu: list = []

    @abstractmethod
    def transform(self, *args, **kwargs):
        raise NotImplementedError(METHOD_NOT_IMPLEMENTED)

    def get_transformed(self) -> list[dict]:
        return self.accu

    def clear(self):
        self.accu = []


class MongoDTO(AbstractDTO):
    def transform(self, source: BaseModel) -> NoReturn:
        record: dict = source.model_dump(exclude={"id"})
        self.accu.append(record)


class InfluxDTO(AbstractDTO):
    def transform(self, source: BaseModel) -> NoReturn:
        measurement: dict = {"measurement": "data_graduates", "fields": source.model_dump(exclude={"id"}), }
        self.accu.append(measurement)


class ClickhouseDTO(AbstractDTO):
    def transform(self, source: BaseModel) -> NoReturn:
        years = str(source.year)
        years = datetime.strptime(years, "%Y")

        record = source.model_dump(include={"average_salary", "percent_employed", "id"}, )

        record["years"] = years
        record["Sign"] = 1

        self.accu.append(record)


WORKERS = [MongoDTO, InfluxDTO, ClickhouseDTO]


class InterfaceDTO:
    def __init__(self) -> NoReturn:
        self.workers: list[AbstractDTO] = [worker() for worker in WORKERS]

    def transform(self, source: BaseModel) -> NoReturn:
        for worker in self.workers:
            worker.transform(source)

    def get_transformed(self) -> Generator:
        for worker in self.workers:
            yield worker.get_transformed()

    def clear(self):
        for worker in self.workers:
            worker.clear()
