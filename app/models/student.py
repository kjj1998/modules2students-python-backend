"""Pydantic models definition.

This package contains the Pydantic model defintiions used for students.

"""
from typing import Union
from pydantic import BaseModel


class Student(BaseModel):
    """Base Model for representing students.

    This is a Pydantic model to represent students.

    Attributes:
      student_id:
        The student id represented as a string.
      email:
        The email of the student represented as a string.
      major:
        The major of the student represented as a string.
      first_name:
        The first name of the student represented as a string.
      last_name:
        The last name of the student represented as a string.
      year_of_study:
        The student's year of study represented as an integer.
      disciplines:
        The disciplines which the student belongs to represented as
        a list of strings.
      course_codes:
        The modules that the student have taken represented as a list of
        strings where the strings are the course codes of the taken modules.
    """

    student_id: str
    email: str
    major: Union[str, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    year_of_study: int = 1
    disciplines: Union[list[str], None] = None
    course_codes: Union[list[str], None] = None


class StudentDB(Student):
    """DB Model for representing students.

    This is a Pydantic model to represent students in the db.

    Attributes:
      password:
        The password of this user account.
    """

    password: str
