"""Pydantic models definition"""
from typing import Union
from pydantic import BaseModel

class ModuleCourseCodeAndName(BaseModel):
    """Course code and name model"""

    course_code: str
    course_name: str

class ModuleBase(BaseModel):
    """
    Base model for modules
    """

    course_code: str
    course_name: str
    course_info: Union[str, None] = None
    academic_units: int = None
    broadening_and_deepening: bool = None
    faculty: str = None
    grade_type: str = None
    total: Union[int, None] = None
    prerequisites: Union[list[list[str]], None] = None
    mutually_exclusives: Union[list[str], None] = None

class StudentBase(BaseModel):
    """
    Base Model for students
    """

    student_id: str
    email: str
    major: str = ""
    first_name: str = ""
    last_name: str = ""
    year_of_study: int = 1
    disciplines: list[str] = []
    course_codes: list[str] = []
