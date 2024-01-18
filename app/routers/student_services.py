"""CRUD utility functions for student endpoints.
"""

from collections import deque
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from neo4j import Driver
from jose import JWTError, jwt

import config # pylint: disable=import-error

from . import db_functions
from .models import StudentBase, ModuleBase

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = config.Settings()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_student(
    student_id: str, driver: Driver, token: Annotated[str, Depends(oauth2_scheme)]
) -> StudentBase:
    """Retrieve a student's information from the db.

    This function retrieves a student's information from the db
    based on the student id supplied. The function takes in the
    student id and an open instance of the neo4j.Driver.

    Args:
      student_id:
        The id of the student whose information we want to retrieve.
      driver:
        An open instance of the neo4j.Driver.
      token:
        JWT access token.

    Returns:
      The information of the student encapsulated in a StudentBase model.
      Raises exceptions if there is an error.
    """
    username: str = ""

    try:
        payload: dict[str, any] = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username = payload.get("user_id")
        if username is None or username != student_id:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    student: StudentBase = db_functions.get_student(username, driver)

    if student is None:
        raise credentials_exception

    return student


async def update_student_details(
    student_update: StudentBase, driver: Driver, token: Annotated[str, Depends(oauth2_scheme)]
) -> StudentBase:
    """Updates the details of the student in the db.

    Updates the details of the student in the db with the information
    given in the student parameter.

    Args:
      student_update:
        A StudentBase model containing the information used to update the student's details.
      driver:
        An open instance of the neo4j.Driver.
      token:
        JWT access token.

    Returns:
      A StudentBase model containing the updated information.
    """
    username: str = ""

    try:
        payload: dict[str, any] = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username = payload.get("user_id")
        if username is None or username != student_update.student_id:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    cur_student: StudentBase = db_functions.get_student(username, driver)

    if cur_student is None:
        raise credentials_exception

    updated_modules_course_codes: list[str] = student_update.course_codes
    updated_modules: list[ModuleBase] = db_functions.get_modules_based_on_course_codes(
        updated_modules_course_codes, driver)

    if len(updated_modules_course_codes) != len(updated_modules):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some of the course codes are invalid",
        )

    course_codes_of_eligible_modules: list[str] = check_prerequisites_fulfillment(
        updated_modules, driver)

    if len(course_codes_of_eligible_modules) != len(updated_modules_course_codes):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prerequisites have not been fulfilled for some of the modules."
        )

    updated_student: StudentBase = db_functions.update_student(student_update, driver)

    updated_modules_course_codes = update_student_modules(
        student_update.student_id, student_update.course_codes, driver
    )
    updated_student.course_codes = updated_modules_course_codes

    return updated_student

def search_for_modules(modules: list[str], driver: Driver) -> list[str]:
    """Checks whether a list of modules exist in the db.

    Checks whether a list of modules exist in the db by searching for their
    course codes.

    Args:
      modules:
        A list of strings containing the course codes of the modules to be
        checked.
      driver:
        An open instance of a neo4j.Driver.

    Returns:
      A list of strings containing the course codes of modules that exist in
      the db.
    """

    return db_functions.search_for_modules(modules, driver)


def check_modules_existence(modules: list[str], driver: Driver) -> bool:
    """Function to check whether the list of modules exist in the db"""
    retrieved_modules: list[str] = db_functions.search_for_modules(modules, driver)

    return len(retrieved_modules) == len(modules)


def update_student_modules(student_id: str, modules: list[str], driver: Driver) -> list[str]:
    """Function to update the modules of a student"""

    if check_modules_existence(modules, driver) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some of the course codes entered are invalid!",
        )

    current_modules: list[ModuleBase] = db_functions.get_modules_currently_taken(student_id, driver)
    current_modules_set: set[str] = set(current_module.course_code
                                        for current_module in current_modules)
    new_modules_set: set[str] = set(modules)
    modules_to_be_removed: list[str] = list(current_modules_set.difference(new_modules_set))
    modules_to_be_added: list[str] = list(new_modules_set.difference(current_modules_set))

    db_functions.remove_modules(student_id, modules_to_be_removed, driver)
    db_functions.add_modules(student_id, modules_to_be_added, driver)

    return modules


def check_prerequisites_fulfillment(modules: list[ModuleBase], driver: Driver) -> list[str]: # pylint: disable=too-many-locals
    """Checks whether the list of modules fulfil their prerequisites.

    Checks whether the list of modules fulfil their prerequisites that is to
    say all modules in the list are eligible and if a module has prerequisites, 
    it prerequisite modules are also in this list

    Args:
      modules:
        The list of modules to be checked.

    Returns:
      list of modules that are eligible.
    
    """
    in_degree: dict[str, list[set[str]]] = {}
    out_degree: dict[str, list[str]] = {}

    for module in modules:
        current_course_code: str = module.course_code
        prereq_groups: list[list[str]] = module.prerequisites

        in_degree[current_course_code] = []

        if prereq_groups is not None and prereq_groups:
            for prerequisite_group in prereq_groups:
                prereq_modules: list[ModuleBase] = db_functions.get_modules_based_on_course_codes(
                    prerequisite_group, driver)

                for prereq_module in prereq_modules:
                    if prereq_module.course_code not in out_degree:
                        out_degree[prereq_module.course_code] = []

                    out_degree[prereq_module.course_code].append(current_course_code)

                in_degree[current_course_code].append(
                    set(prereq_module.course_code for prereq_module in prereq_modules)
                )

    course_codes_of_eligible_modules: list[str] = []
    queue: deque[str] = deque()

    for course_code in in_degree.items():
        if in_degree[course_code] is None or len(in_degree[course_code]) == 0:
            queue.append(course_code)

    while len(queue) > 0:
        cur_course_code: str = queue.popleft()
        course_codes_of_eligible_modules.append(cur_course_code)

        next_modules: list[str] = out_degree[cur_course_code]

        if next_modules is not None and len(next_modules) > 0:
            for next_module in next_modules:
                prereq_groups: list[set[str]] = in_degree[next_module]

                for prereq_group in prereq_groups:
                    prereq_group.remove(cur_course_code)

                    if len(prereq_group) == 0:
                        queue.append(next_module)
                        in_degree[next_module] = []
                        break

    return course_codes_of_eligible_modules
