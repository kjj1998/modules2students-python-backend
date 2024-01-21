"""
Functions to interact with the db for recommendations
"""

from neo4j import Driver, Record, EagerResult

from ..queries.rec_cypher_queries import (
    GET_CB_MODULES_THAT_FULFILL_PREREQS,
    GET_CB_MODULES_WITH_NO_PREREQS,
    GET_CF_MODULES_THAT_FULFILL_PREREQS,
    GET_CF_MODULES_WITH_NO_PREREQS,
)

from ..models.module import Module


def get_cb_recs_that_fulfil_prereq(student_id: str, driver: Driver) -> list[Module]:
    """Function to get content-based recommendations that fulfil prerequisites."""
    query: str = GET_CB_MODULES_THAT_FULFILL_PREREQS

    eager_result: EagerResult = driver.execute_query(
        query,
        student_id=student_id,
        database_="neo4j",
    )

    records: list[Record] = eager_result.records
    modules: list[Module] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: Module = Module(**data)
        modules.append(module)

    return modules


def get_cb_recs_that_have_no_prereq(student_id: str, driver: Driver) -> list[Module]:
    """Function to get content-based recommendations that have no prerequisites."""
    query: str = GET_CB_MODULES_WITH_NO_PREREQS

    eager_result: EagerResult = driver.execute_query(
        query, student_id=student_id, database_="neo4j"
    )

    records: list[Record] = eager_result.records
    modules: list[Module] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: Module = Module(**data)
        modules.append(module)

    return modules


def get_cf_recs_that_fulfill_prereq(student_id: str, driver: Driver) -> list[Module]:
    """Function to get collaborative filtering recommendations that fulfill prerequisites."""
    query: str = GET_CF_MODULES_THAT_FULFILL_PREREQS

    eager_result: EagerResult = driver.execute_query(
        query, student_id=student_id, database_="neo4j"
    )

    records: list[Record] = eager_result.records
    modules: list[Module] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: Module = Module(**data)
        modules.append(module)

    return modules


def get_cf_recs_that_have_no_prereq(student_id: str, driver: Driver) -> list[Module]:
    """Function to get collaborative filtering recommendations that have no prerequisites."""
    query: str = GET_CF_MODULES_WITH_NO_PREREQS

    eager_result: EagerResult = driver.execute_query(
        query, student_id=student_id, database_="neo4j"
    )

    records: list[Record] = eager_result.records
    modules: list[Module] = []

    for record in records:
        data: dict[str, any] = record.data()
        module: Module = Module(**data)
        modules.append(module)

    return modules
