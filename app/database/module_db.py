"""
Functions to interact with the db for module data
"""

from neo4j import Driver, Record, EagerResult

from ..queries.module_cypher_queries import (
    GET_ALL_MODULES,
    GET_MODULE,
    SEARCH_MODULES,
    GET_MODULES_COURSE_CODES,
    GET_FACULTIES,
    GET_PREREQUISITE_GROUPS_FOR_EACH_MODULE,
    GET_MUTUALLY_EXCLUSIVES_FOR_EACH_MODULE,
    GET_MODULES_FOR_A_FACULTY,
    GET_TOTAL_NUMBER_OF_MODULES,
)

from ..models.module import Module, ModuleCourseCodeAndName


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
    query: str = GET_ALL_MODULES

    eager_result: EagerResult = driver.execute_query(
        query,
        skip=skip,
        limit=limit,
        database_="neo4j",
    )
    records: list[Record] = eager_result.records
    modules: list[Module] = []

    for record in records:
        data = record.data()
        module: Module = Module(**data)
        prereqs: list[list[str]] = get_prerequisite_groups_for_each_module(
            data["course_code"], driver
        )
        mutuallly_exclusives: list[str] = get_mutually_exclusives_for_each_module(
            data["course_code"], driver
        )
        module.prerequisites = prereqs
        module.mutually_exclusives = mutuallly_exclusives
        modules.append(module)

    return modules


def get_modules_based_on_course_codes(
    course_codes: list[str], driver: Driver
) -> list[Module]:
    """Retreive modules based on their course codes."""
    modules: list[Module] = []

    for course_code in course_codes:
        module: Module = get_module(course_code, driver)
        if module is not None:
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
    query: str = GET_MODULE

    eager_result: EagerResult = driver.execute_query(
        query,
        course_code=course_code,
        database_="neo4j",
    )
    records: list[Record] = eager_result.records
    module: Module = None

    if len(records) == 0:
        return None

    data: dict[str, any] = records[0].data()
    module: Module = Module(**data)
    prerequisites: list[list[str]] = get_prerequisite_groups_for_each_module(
        course_code, driver
    )
    mutually_exclusives: list[str] = get_mutually_exclusives_for_each_module(
        course_code, driver
    )

    module.prerequisites = prerequisites
    module.mutually_exclusives = mutually_exclusives

    return module


def search_modules(
    search_term: str, skip: int, limit: int, driver: Driver
) -> list[Module]:
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
    query: str = SEARCH_MODULES

    eager_result: EagerResult = driver.execute_query(
        query,
        search_term=f"*{search_term}*",
        skip=skip,
        limit=limit,
        database_="neo4j",
    )
    records: list[Record] = eager_result.records
    modules: list[Module] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: Module = Module(**data)
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
    query: str = GET_MODULES_COURSE_CODES

    eager_result: EagerResult = driver.execute_query(query, database_="neo4j")
    records: list[Record] = eager_result.records
    course_codes: list[str] = []

    for record in records:
        data: dict[str, any] = record.data()
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
    query: str = GET_FACULTIES

    eager_result: EagerResult = driver.execute_query(query, database_="neo4j")
    records: list[Record] = eager_result.records
    faculties: list[str] = []

    for record in records:
        data: dict[str, any] = record.data()
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
    query: str = GET_MODULES_FOR_A_FACULTY

    eager_result: EagerResult = driver.execute_query(
        query, faculty=faculty, database_="neo4j"
    )
    records: list[Record] = eager_result.records
    modules: list[ModuleCourseCodeAndName] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: ModuleCourseCodeAndName = ModuleCourseCodeAndName(**data)
        modules.append(module)

    return modules


def get_total_number_of_modules(driver: Driver) -> int:
    """Retrieve the total number of modules.

    Args:
      driver:
        An open instance of the neo4j.Driver.

    Returns:
      The total number of modules in the db.
    """
    query: str = GET_TOTAL_NUMBER_OF_MODULES

    eager_result: EagerResult = driver.execute_query(query, database_="neo4j")
    records: list[Record] = eager_result.records

    return records[0].data()["total"]


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
    search_for_modules_query: str = GET_MODULE
    retrieved_modules: list[str] = []

    for module in modules:
        eager_result: EagerResult = driver.execute_query(
            search_for_modules_query,
            course_code=module,
            database_="neo4j",
        )
        records: list[Record] = eager_result.records

        if len(records) == 0:
            continue

        data: dict[str, any] = records[0].data()
        retrieved_modules.append(data["course_code"])

    return retrieved_modules
