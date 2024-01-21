"""
Functions to interact with the db for auth
"""

from neo4j import Driver

from ..queries.auth_cypher_queries import REGISTER_USER
from ..models.student import StudentDB


def register_student(new_student: StudentDB, hashed_password: str, driver: Driver):
    """Function to register a student in the db."""
    query: str = REGISTER_USER

    driver.execute_query(
        query,
        student_id=new_student.student_id,
        email=new_student.email,
        password=hashed_password,
        major=new_student.major,
        first_name=new_student.first_name,
        last_name=new_student.last_name,
        year_of_study=new_student.year_of_study,
        disciplines=new_student.disciplines,
        database_="neo4j",
    )
