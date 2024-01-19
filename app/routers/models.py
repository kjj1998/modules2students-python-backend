"""Pydantic models definition.

This package contains the Pydantic model defintiions used.

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


class ModuleBase(BaseModel):
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


# class PrerequisiteGroup(BaseModel):
#     """
#     Model for prerequisite groups
#     """

#     group_id: str
#     modules: list[ModuleBase]


# class ModuleDTO(ModuleBase):
#     """
#     Model for module for data transfer to frontend
#     """

#     prerequisites: Union[list[list[str]], None] = None
#     mutually_exclusives: Union[list[str], None] = None


# class ModuleDB(ModuleBase):
#     """
#     Model for modules in DB
#     """

#     prerequisites: Union[list[PrerequisiteGroup], None] = None


class StudentBase(BaseModel):
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


class StudentDB(StudentBase):
    """DB Model for representing students.

    This is a Pydantic model to represent students in the db.

    Attributes:
      password:
        The password of this user account.
    """

    password: str


class RegistrationModel(BaseModel):
    """Model for registration of new users.

    This is a Pydantic model for the registration of new users.

    Attributes:
      student_id:
        The student id is represented as a string.
      password:
        The password is represented as a string.
      email:
        The email is represented as a string.
    """

    student_id: str
    password: str
    email: str


class AuthenticationModel(BaseModel):
    """Model to login and authenticate existing users.

    This is a Pydantic model for login of existing users.

    Attributes:
      username:
        The username of the user which is the student id.
      password:
        The password represented as a string.
    """

    username: str
    password: str


class AuthenticationResponseModel(BaseModel):
    """Model for authentication response of users.

    This is a Pydantic model for the response after authentication of users.

    Attributes:
      access_token:
        The JWT token represented as a string.
      user_id:
        The ID of the user represented as a string.
    """

    access_token: str
    user_id: str


class RecommendationModel(BaseModel):
    """Model for recommendations

    This is a Pydantic model for the modules recommendations of users.

    Attributes:
      cf_recommendations:
        The list of modules recommended through collaborative filtering.
      cbf_recommendations:
        The list of modules recommended through content-based filtering.
    """

    cf_recommendations: list[ModuleBase] = []
    cbf_recommendations: list[ModuleBase] = []
