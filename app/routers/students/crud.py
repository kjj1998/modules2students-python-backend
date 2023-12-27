"""CRUD utility functions for student endpoints"""

from neo4j import Driver
from . import cypher_queries, models


def get_student(student_id: str, driver: Driver):
    """Function to get a single student from Neo4j db"""
    query = cypher_queries.GET_STUDENT

    eager_result = driver.execute_query(
        query,
        student_id=student_id,
        database_="neo4j",
    )
    records = eager_result.records
    student: models.StudentBase = None

    if len(records) == 0:
        return None

    data = records[0].data()
    student = models.StudentBase(**data)
    modules_taken = get_student_courses(student_id, driver)
    student.course_codes = modules_taken

    return student


def get_student_courses(student_id: str, driver: Driver):
    """Function to get the modules that each student is taking"""
    query = cypher_queries.GET_STUDENT_MODULES

    eager_result = driver.execute_query(query, student_id=student_id, database_="neo4j")
    records = eager_result.records
    modules: list[str] = []

    for record in records:
        data = record.data()
        modules.append(data["course_code"])

    return modules
