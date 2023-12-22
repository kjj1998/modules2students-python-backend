"""CRUD utilities function"""

from neo4j import Driver
from . import queries, models

def get_modules(skip: int, limit: int, driver: Driver):
    """Function to get modules data from Neo4j db"""
    query = queries.GET_ALL_MODULES

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
