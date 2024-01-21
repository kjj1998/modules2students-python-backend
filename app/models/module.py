"""Pydantic models definition.

This package contains the Pydantic model defintiions used for modules.

"""
from typing import Union
from pydantic import BaseModel


class ModuleCourseCodeAndName(BaseModel):
    """Course code and name model

    This is a Pydantic model containing the course code and
    course name of a module.

    Attributes:
      course_code:
        The course code of the module represented as a string.
      course_name:
        The name of the module represented as a string.
    """

    course_code: str
    course_name: str


class Module(BaseModel):
    """Base model for representing modules.

    This is a Pydantic model to represent modules.

    Attributes:
      course_code:
        The course code of the module represented as
        a string.
      course_name:
        The name of the module represented as a string.
      course_info:
        The background information of the module represented
        as a string.
      academic_units:
        The number of academic units the module is worth.
      broadening_and_deepening:
        A boolean indicating whether the module
        qualifies as a broadening and deepening elective.
      faculty:
        The faculty which the module belongs to represented
        as a string
      grade_type:
        The grade type of the module represented as a string.
      total:
        The total number of modules retrieved in this API call, to be used
        for pagination. Represented as an integer.
      prerequisites:
        The groups of modules that are prerequisites for this module. Represented
        as a list of list of strings where the strings are the course codes of the
        prerequisite modules.
      mutually_exclusives:
        The modules that are mutually exclusive to this module. Represented as
        a list of strings where the strings are the course codes of the mutually
        exclusive modules.
    """

    course_code: str
    course_name: str
    course_info: Union[str, None] = None
    academic_units: int = None
    broadening_and_deepening: bool = None
    faculty: str = None
    grade_type: str = None
    total: Union[int, None] = None
    prerequisites: list[list[str]] = []
    mutually_exclusives: list[str] = []
    score: float = 0.0
