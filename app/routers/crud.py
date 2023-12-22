"""CRUD utilities function"""

from neo4j import Driver
from . import cypher_queries, models

def get_modules(skip: int, limit: int, driver: Driver):
    """Function to get modules data from Neo4j db"""
    query = cypher_queries.GET_ALL_MODULES

    eager_result = driver.execute_query(
        query,
        skip=skip,
        limit=limit,
        database_="neo4j",
    )
    records = eager_result.records
    modules: list[models.ModuleBase] = []

    for record in records:
        data = record.data()
        module = models.ModuleBase(**data)
        modules.append(module)

    return modules

def get_module(course_code: str, driver: Driver):
    """Function get a single module data from Neo4j db"""
    query = cypher_queries.GET_MODULE

    eager_result = driver.execute_query(
        query,
        course_code=course_code,
        database_="neo4j",
    )
    records = eager_result.records
    module: models.ModuleBase = None

    if len(records) > 0:
        data = records[0].data()
        module = models.ModuleBase(**data)

    return module

def search_modules(search_term: str, skip: int, limit: int, driver: Driver):
    """Function to search for modules in the db"""
    query = cypher_queries.SEARCH_MODULES

    eager_result = driver.execute_query(
        query,
        search_term=search_term,
        skip=skip,
        limit=limit,
        database_="neo4j",
    )
    records = eager_result.records
    modules: list[models.ModuleBase] = []

    for record in records:
        data = record.data()
        module = models.ModuleBase(**data)
        modules.append(module)

    return modules

def get_modules_course_codes(driver: Driver):
    """Function to get all modules' course codes"""
    query = cypher_queries.GET_MODULES_COURSE_CODES

    eager_result = driver.execute_query(
        query,
        database_="neo4j"
    )
    records = eager_result.records
    course_codes: list[str] = []

    for record in records:
        data = record.data()
        course_codes.append(data["course_code"])

    return course_codes

def get_faculties(driver: Driver):
    """Function to get all faculties"""
    query = cypher_queries.GET_FACULTIES

    eager_result = driver.execute_query(
        query,
        database_="neo4j"
    )
    records = eager_result.records
    faculties: list[str] = []

    for record in records:
        data = record.data()
        faculties.append(data["faculty"])

    return faculties

def get_modules_in_a_faculty(faculty: str, driver: Driver):
    """Function to get all modules in a faculty"""
    query = cypher_queries.GET_MODULES_FOR_A_FACULTY

    eager_result = driver.execute_query(
        query,
        faculty=faculty,
        database_="neo4j"
    )
    records = eager_result.records
    modules: list[models.ModuleBase] = []

    for record in records:
        data = record.data()
        module = models.ModuleBase(**data)
        modules.append(module)

    return modules
