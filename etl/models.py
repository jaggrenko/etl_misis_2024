from typing import Any, Optional
from pydantic import AliasPath, BaseModel, Field


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
