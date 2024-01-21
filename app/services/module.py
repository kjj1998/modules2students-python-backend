"""CRUD utility functions for modules.

This module contains the CRUD utility functions that
deals with modules

"""

from neo4j import Driver, EagerResult, Record

from ..database import module_db
from ..models.module import Module, ModuleCourseCodeAndName
from ..queries.module_cypher_queries import (
    GET_PREREQUISITE_GROUPS_FOR_EACH_MODULE,
    GET_MUTUALLY_EXCLUSIVES_FOR_EACH_MODULE,
)


def get_modules(skip: int, limit: int, driver: Driver) -> list[Module]:
    """Retrieves modules from the db.

    Retrieves modules from the db based on the
    skip and limit values supplied.

    Args:
      skip:
        The number of modules to be skipped when retrieving.
      limit:
        The number of modules to be retrieved.
      driver:
        An open instance of neo4j.Driver

    Returns:
      A list of Modules
    """

    return module_db.get_modules(skip, limit, driver)


def get_module(course_code: str, driver: Driver) -> Module:
    """Retrieves a single module from the db

    Retrieves a single module from the db based
    on the supplied course code.

    Args:
      course_code:
        The course code of the module to be retrieved.
      driver:
        An open instance of neo4j.Driver

    Returns:
      The retrieved module or None if no such module with the
      given course code exists.
    """

    return module_db.get_module(course_code, driver)


def search_modules(search_term: str, skip: int, limit: int, driver: Driver) -> list[Module]:
    """Searches for modules based on a search term.

    Searches for relevant modules based on the provided search term.
    The number of relevant modules to be returned can be adjusted using
    the skip and limit parameters provided.

    Args:
      search_term:
        The search term used to search for relevant modules
      skip:
        The number of modules to be skipped
      limit:
        The number of modules to be returned
      driver:
        An open instance of neo4j.Driver

    Returns:
      A list of modules that are relevant to the search term.
    """

    return module_db.search_modules(search_term, skip, limit, driver)


def get_modules_course_codes(driver: Driver) -> list[str]:
    """Retrieves all course codes of all modules in the db.

    Retrieves the course codes for all of the modules in
    the db.

    Args:
      driver:
        An open neo4j.Driver instance.

    Returns:
      A list of course codes of all the modules in the db.
    """

    return module_db.get_modules_course_codes(driver)


def get_faculties(driver: Driver) -> list[str]:
    """Retrieves all the faculties of modules.

    Retrieves all faculties which modules can belong to
    from the db.

    Args:
      driver:
        An open instance of neo4j.Driver.

    Returns:
      A list of all the faculties that modules can belong to.
    """

    return module_db.get_faculties(driver)


def get_modules_in_a_faculty(faculty: str, driver: Driver) -> list[ModuleCourseCodeAndName]:
    """Retrieves all modules that belong to a faculty.

    Retrieves all modules that belong to a specific faculty
    from the db. The pariticular faculty is supplied as a
    function parameter.

    Args:
      faculty:
        The faculty which modules shall be retrieved.
      driver:
        An open instance of the neo4j.Driver.

    Returns:
      A list of all modules that belong to a specific faculty.
    """

    return module_db.get_modules_in_a_faculty(faculty, driver)


def get_prerequisite_groups_for_each_module(course_code: str, driver: Driver) -> list[list[str]]:
    """Retrieves all prerequisite groups for a module.

    Retrieves all prerequisite groups for a module which is
    specified by the provided course code.

    Args:
      course_code:
        Course code of the module from which to retreive
        its prerequisite groups.
      driver:
        An open instance of a neo4j.Driver.

    Returns:
      A list of list of strings. Each inner list contains the course codes
      that make up that particular prerequisite group.
    """
    query: str = GET_PREREQUISITE_GROUPS_FOR_EACH_MODULE

    eager_result: EagerResult = driver.execute_query(
        query, course_code=course_code, database_="neo4j"
    )
    records: list[Record] = eager_result.records
    prerequisite_groups: list[list[str]] = []

    for record in records:
        data: dict[str, any] = record.data()
        prerequisite_groups.append(data["prereqInfo"])

    return prerequisite_groups


def get_mutually_exclusives_for_each_module(course_code: str, driver: Driver) -> list[str]:
    """
    Retreive the modules that are mutually exclusive to the current module.

    The modules that are mutually exclusive to the specified module will be retrieved.

    Args:
      course_code:
        The course code of the module for which its mutually exclusive modules
        will be retrieved.
      driver:
        An open instance of the neo4j.Driver.

    Returns:
      A list of course codes of the mutually exclusive modules.
    """
    query: str = GET_MUTUALLY_EXCLUSIVES_FOR_EACH_MODULE

    eager_result: EagerResult = driver.execute_query(
        query, course_code=course_code, database_="neo4j"
    )
    records: list[Record] = eager_result.records
    mutually_exclusives: list[str] = []

    for record in records:
        data: dict[str, any] = record.data()
        mutually_exclusives.append(data["mutualCourseCode"])

    return mutually_exclusives


def get_total_number_of_modules(driver: Driver) -> int:
    """Retrieve the total number of modules.

    Args:
      driver:
        An open instance of the neo4j.Driver.

    Returns:
      The total number of modules in the db.
    """

    return module_db.get_total_number_of_modules(driver)
