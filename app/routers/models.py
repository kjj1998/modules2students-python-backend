"""Pydantic models definition"""
from typing import Union
from pydantic import BaseModel

class ModuleBase(BaseModel):
    """
    Base model for modules
    """

    course_code: str
    course_name: str
    course_info: Union[str, None] = None
    academic_units: int
    broadening_and_deepening: bool
    faculty: str
    grade_type: str
    total: Union[int, None] = None
