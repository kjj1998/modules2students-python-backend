"""Pydantic models definition for student"""
from typing import Union
from pydantic import BaseModel

class StudentBase(BaseModel):
    """
    Base Model for students
    """

    student_id: str
    email: str
    major: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    year_of_study: Union[int, None] = None
    disciplines: Union[list[str], None] = None
    course_codes: Union[list[str], None] = None

