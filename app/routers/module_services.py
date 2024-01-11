"""CRUD utility functions for modules.

This module contains the CRUD utility functions that
deals with modules

"""

from neo4j import Driver
from .models import ModuleBase, ModuleCourseCodeAndName
from .module_cypher_queries import (
    GET_ALL_MODULES,
    GET_MODULE,
    SEARCH_MODULES,
    GET_MODULES_COURSE_CODES,
    GET_FACULTIES,
)
from .module_cypher_queries import (
    GET_PREREQUISITE_GROUPS_FOR_EACH_MODULE,
    GET_MUTUALLY_EXCLUSIVES_FOR_EACH_MODULE,
    GET_MODULES_FOR_A_FACULTY,
    GET_TOTAL_NUMBER_OF_MODULES,
)


def get_modules(skip: int, limit: int, driver: Driver) -> list[ModuleBase]:
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
    query = GET_ALL_MODULES

    eager_result = driver.execute_query(
        query,
        skip=skip,
        limit=limit,
        database_="neo4j",
    )
    records = eager_result.records
    modules: list[ModuleBase] = []

    for record in records:
        data = record.data()
        module = ModuleBase(**data)
        prereqs = get_prerequisite_groups_for_each_module(data["course_code"], driver)
        mutuallly_exclusives = get_mutually_exclusives_for_each_module(
            data["course_code"], driver
        )
        module.prerequisites = prereqs
        module.mutually_exclusives = mutuallly_exclusives
        modules.append(module)

    return modules


def get_module(course_code: str, driver: Driver) -> ModuleBase:
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
    query = GET_MODULE

    eager_result = driver.execute_query(
        query,
        course_code=course_code,
        database_="neo4j",
    )
    records = eager_result.records
    module: ModuleBase = None

    if len(records) == 0:
        return None

    data = records[0].data()
    module = ModuleBase(**data)
    prerequisites = get_prerequisite_groups_for_each_module(course_code, driver)
    mutually_exclusives = get_mutually_exclusives_for_each_module(course_code, driver)

    module.prerequisites = prerequisites
    module.mutually_exclusives = mutually_exclusives

    return module


def search_modules(
    search_term: str, skip: int, limit: int, driver: Driver
) -> list[ModuleBase]:
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
    query = SEARCH_MODULES

    eager_result = driver.execute_query(
        query,
        search_term=f"*{search_term}*",
        skip=skip,
        limit=limit,
        database_="neo4j",
    )
    records = eager_result.records
    modules: list[ModuleBase] = []

    for record in records:
        data = record.data()
        module = ModuleBase(**data)
        modules.append(module)

    return modules


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
    query = GET_MODULES_COURSE_CODES

    eager_result = driver.execute_query(query, database_="neo4j")
    records = eager_result.records
    course_codes: list[str] = []

    for record in records:
        data = record.data()
        course_codes.append(data["course_code"])

    return course_codes


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
    query = GET_FACULTIES

    eager_result = driver.execute_query(query, database_="neo4j")
    records = eager_result.records
    faculties: list[str] = []

    for record in records:
        data = record.data()
        faculties.append(data["faculty"])

    return faculties


def get_modules_in_a_faculty(
    faculty: str, driver: Driver
) -> list[ModuleCourseCodeAndName]:
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
    query = GET_MODULES_FOR_A_FACULTY

    eager_result = driver.execute_query(query, faculty=faculty, database_="neo4j")
    records = eager_result.records
    modules: list[ModuleCourseCodeAndName] = []

    for record in records:
        data = record.data()
        module = ModuleCourseCodeAndName(**data)
        modules.append(module)

    return modules


def get_prerequisite_groups_for_each_module(
    course_code: str, driver: Driver
) -> list[list[str]]:
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
    query = GET_PREREQUISITE_GROUPS_FOR_EACH_MODULE

    eager_result = driver.execute_query(
        query, course_code=course_code, database_="neo4j"
    )
    records = eager_result.records
    prerequisite_groups: list[list[str]] = []

    for record in records:
        data = record.data()
        prerequisite_groups.append(data["prereqInfo"])

    return prerequisite_groups


def get_mutually_exclusives_for_each_module(
    course_code: str, driver: Driver
) -> list[str]:
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
    query = GET_MUTUALLY_EXCLUSIVES_FOR_EACH_MODULE

    eager_result = driver.execute_query(
        query, course_code=course_code, database_="neo4j"
    )
    records = eager_result.records
    mutually_exclusives: list[str] = []

    for record in records:
        data = record.data()
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
    query = GET_TOTAL_NUMBER_OF_MODULES

    eager_result = driver.execute_query(query, database_="neo4j")
    records = eager_result.records

    return records[0].data()["total"]
