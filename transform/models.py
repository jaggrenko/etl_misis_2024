from typing import Any, Optional
from pydantic import BaseModel


class DescriptionGraduatesUniversity(BaseModel):
    id: Any
    object_level: str
    object_name: str
    gender: str
    education_level: str
    year: int
    university: str
    special_section: str
    speciality: str
    speciality_code: str
    count_graduate: int
    percent_employed: float
    average_salary: Optional[float] = None
    oktmo: str
    okato: str

    def model_post_init(self, __context: Any) -> None:
        self.average_salary = self.average_salary or 0.0
        # self.average_salary if self.average_salary else 0.0
