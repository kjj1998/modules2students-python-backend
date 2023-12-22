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
