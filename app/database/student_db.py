"""
Functions to interact with the db for user data
"""

from neo4j import Driver, Record, EagerResult

from ..queries.student_cypher_queries import (
    GET_STUDENT,
    GET_STUDENT_MODULES,
    UPDATE_STUDENT,
    DELETE_MODULE_TAKEN,
    ADD_MODULE_TAKEN,
)

from ..models.student import Student, StudentDB
from ..models.module import Module
from .module_db import (
    get_mutually_exclusives_for_each_module,
    get_prerequisite_groups_for_each_module,
)


def get_student(student_id: str, driver: Driver) -> StudentDB:
    """Retrieve a student's information from the db.

    This function retrieves a student's information from the db
    based on the student id supplied. The function takes in the
    student id and an open instance of the neo4j.Driver.

    Args:
      student_id:
        The id of the student whose information we want to retrieve.
      driver:
        An open instance of the neo4j.Driver.

    Returns:
      The information of the student encapsulated in a StudentBase model.
      Returns None if the student does not exist.
    """
    query: str = GET_STUDENT

    eager_result: EagerResult = driver.execute_query(
        query,
        student_id=student_id,
        database_="neo4j",
    )
    records: list[Record] = eager_result.records
    student: StudentDB = None

    if len(records) == 0:
        return None

    data: dict[str, any] = records[0].data()
    student = StudentDB(**data)
    modules_taken: list[str] = get_student_courses(student_id, driver)
    student.course_codes = modules_taken

    return student


def get_student_courses(student_id: str, driver: Driver) -> list[str]:
    """Retrieves the modules that the student has taken.

    This function retrieves the modules that the student has taken represented
    as a list of course codes.

    Args:
      student_id:
        The id of the student from which to retrieve its modules taken.
      driveR:
        An open instance of the neo4j.Driver.

    Returns:
      A list of strings which represent the modules that the student have taken.

    """
    query: str = GET_STUDENT_MODULES

    eager_result: EagerResult = driver.execute_query(
        query, student_id=student_id, database_="neo4j"
    )
    records: list[Record] = eager_result.records
    modules: list[str] = []

    for record in records:
        data: dict[str, any] = record.data()
        modules.append(data["course_code"])

    return modules


def update_student(student_update: Student, driver: Driver) -> Student:
    """Function to update a student in the db.

    This function updates the personal details of the student.

    Args:
      student_update:
        The Student object containing the updated details for that particular student.
      driveR:
        An open instance of the Neo4j driver instance.

    Returns:
      The Student object with the confirmed updated details.

    """
    query: str = UPDATE_STUDENT

    eager_result: EagerResult = driver.execute_query(
        query,
        student_id=student_update.student_id,
        student_email=student_update.email,
        major=student_update.major,
        first_name=student_update.first_name,
        last_name=student_update.last_name,
        year_of_study=student_update.year_of_study,
        email=student_update.email,
        disciplines=student_update.disciplines,
        database_="neo4j",
    )
    records: list[Record] = eager_result.records

    data: dict[str, any] = records[0].data()
    updated_student: Student = Student(**data)

    return updated_student


def remove_modules(student_id: str, modules_to_be_removed: list[str], driver: Driver):
    """Function to remove modules taken by a student.

    This function removes a list of modules taken by the user.

    Args:
      student_id:
        The id of the student.
      modules_to_be_removed:
        The list of modules to be removed represented as course codes.
      driver:
        An open instance of the neo4j driver instance.

    """
    remove_module_taken_query: str = DELETE_MODULE_TAKEN

    for module in modules_to_be_removed:
        driver.execute_query(
            remove_module_taken_query,
            student_id=student_id,
            course_code=module,
            database_="neo4j",
        )


def add_modules(student_id: str, modules_to_be_added: list[str], driver: Driver):
    """Function to add new modules taken by a student

    This function adds a list of modules for the user.

    Args:
      student_id:
        The id of the student.
      modules_to_be_added:
        The list of modules to be added, represented as course codes.
      driver:
        An open instance of the Neo4j driver instance.

    """
    add_module_taken_query: str = ADD_MODULE_TAKEN

    for module in modules_to_be_added:
        driver.execute_query(
            add_module_taken_query,
            student_id=student_id,
            course_code=module,
            database_="neo4j",
        )


def get_modules_currently_taken(student_id: str, driver: Driver) -> list[Module]:
    """Function to retrieve a list of modules currently taken by the user."""
    get_current_modules_query: str = GET_STUDENT_MODULES

    current_modules_eager_result: EagerResult = driver.execute_query(
        get_current_modules_query, student_id=student_id, database_="neo4j"
    )
    records: list[Record] = current_modules_eager_result.records
    current_modules: list[Module] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: Module = Module(**data)
        course_code: str = module["course_code"]
        prerequisites: list[list[str]] = get_prerequisite_groups_for_each_module(
            course_code, driver
        )
        mutually_exclusives: list[str] = get_mutually_exclusives_for_each_module(
            course_code, driver
        )

        module.prerequisites: list[list[str]] = prerequisites
        module.mutually_exclusives: list[str] = mutually_exclusives
        current_modules.append(module)

    return current_modules
