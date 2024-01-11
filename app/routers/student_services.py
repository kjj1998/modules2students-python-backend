"""CRUD utility functions for student endpoints"""

from fastapi import HTTPException, status
from neo4j import Driver
from .models import StudentBase, ModuleBase, PrerequisiteGroup, ModuleDB, ModuleDTO
from .student_cypher_queries import GET_STUDENT, GET_STUDENT_MODULES, UPDATE_STUDENT
from .student_cypher_queries import DELETE_MODULE_TAKEN, ADD_MODULE_TAKEN
from .module_cypher_queries import GET_MODULE
from .module_services import (
    get_mutually_exclusives_for_each_module, get_prerequisite_groups_for_each_module
)

def get_student(student_id: str, driver: Driver) -> StudentBase:
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
    query = GET_STUDENT

    eager_result = driver.execute_query(
        query,
        student_id=student_id,
        database_="neo4j",
    )
    records = eager_result.records
    student: StudentBase = None

    if len(records) == 0:
        return None

    data = records[0].data()
    student = StudentBase(**data)
    modules_taken = get_student_courses(student_id, driver)
    student.course_codes = modules_taken

    return student


def get_student_courses(student_id: str, driver: Driver) -> list[str]:
    """Function to get the modules that each student is taking"""
    query = GET_STUDENT_MODULES

    eager_result = driver.execute_query(query, student_id=student_id, database_="neo4j")
    records = eager_result.records
    modules: list[str] = []

    for record in records:
        data = record.data()
        modules.append(data["course_code"])

    return modules


def update_student_details(student: StudentBase, driver: Driver) -> StudentBase:
    """Function to update the details of a student"""
    query = UPDATE_STUDENT

    eager_result = driver.execute_query(
        query,
        student_id=student.student_id,
        student_email=student.email,
        major=student.major,
        first_name=student.first_name,
        last_name=student.last_name,
        year_of_study=student.year_of_study,
        email=student.email,
        disciplines=student.disciplines,
        database_="neo4j",
    )
    records = eager_result.records

    data = records[0].data()
    updated_student = StudentBase(**data)
    updated_modules = update_student_modules(
        student.student_id, student.course_codes, driver
    )
    updated_student.course_codes = updated_modules

    return updated_student


def search_for_modules(modules: list[str], driver: Driver) -> list[str]:
    """Function to check whether the modules exist in the db"""
    search_for_modules_query = GET_MODULE
    retrieved_modules: list[str] = []

    for module in modules:
        eager_result = driver.execute_query(
            search_for_modules_query,
            course_code=module,
            database_="neo4j",
        )
        records = eager_result.records

        if len(records) == 0:
            continue

        data = records[0].data()
        retrieved_modules.append(data["course_code"])

    return retrieved_modules


def check_modules_existence(modules: list[str], driver: Driver) -> bool:
    """Function to check whether the list of modules exist in the db"""
    retrieved_modules = search_for_modules(modules, driver)

    return len(retrieved_modules) == len(modules)


def get_current_modules_taken(student_id: str, driver: Driver) -> list[ModuleBase]:
    """Function to retrieve a list of modules currently taken by the user"""
    get_current_modules_query = GET_STUDENT_MODULES

    current_modules_eager_result = driver.execute_query(
        get_current_modules_query, student_id=student_id, database_="neo4j"
    )
    records = current_modules_eager_result.records
    current_modules: list[ModuleBase] = []

    for record in records:
        data = record.data()
        module = ModuleBase(**data)
        course_code = module['course_code']
        prerequisites = get_prerequisite_groups_for_each_module(course_code, driver)
        mutually_exclusives = get_mutually_exclusives_for_each_module(course_code, driver)

        module.prerequisites = prerequisites
        module.mutually_exclusives = mutually_exclusives
        current_modules.append(module)

    return current_modules


def remove_modules_taken(student_id: str, modules_to_be_removed: list[str], driver: Driver):
    """Function to remove modules taken by a student"""
    remove_module_taken_query = DELETE_MODULE_TAKEN

    for module in modules_to_be_removed:
        driver.execute_query(
            remove_module_taken_query,
            student_id=student_id,
            course_code=module,
            database_="neo4j",
        )


def add_modules_taken(student_id: str, modules_to_be_added: list[str], driver: Driver):
    """Function to add new modules taken by a student"""
    add_module_taken_query = ADD_MODULE_TAKEN

    for module in modules_to_be_added:
        driver.execute_query(
            add_module_taken_query,
            student_id=student_id,
            course_code=module,
            database_="neo4j",
        )


def update_student_modules(student_id: str, modules: list[str], driver: Driver) -> StudentBase:
    """Function to update the modules of a student"""

    if check_modules_existence(modules, driver) is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Some of the course codes entered are invalid!",
        )


    current_modules = get_current_modules_taken(student_id, driver)
    current_modules_set = set(current_module.course_code for current_module in current_modules)
    new_modules_set = set(modules)
    modules_to_be_removed = list(current_modules_set.difference(new_modules_set))
    modules_to_be_added = list(new_modules_set.difference(current_modules_set))

    remove_modules_taken(student_id, modules_to_be_removed, driver)
    add_modules_taken(student_id, modules_to_be_added, driver)

    return modules

# def check_prerequisites_fulfillment(modules: list[ModuleDB]) -> list[str]:
#     in_degree: dict[str, list[set[str]]] = {}
#     out_degree: dict[str, list[str]] = {}

#     for module in modules:
#         current_course_code: str = module.course_code
#         prereq_groups: list[PrerequisiteGroup] = module.prerequisites
    
#         in_degree[current_course_code] = []

#         if (prereq_groups is not None and prereq_groups):
#             for prerequisite_group in prereq_groups:
#                 prereq_modules: list[ModuleDB] = prerequisite_group.modules

#                 for prereq_module in prereq_modules:
#                     if prereq_module.course_code not in out_degree:
#                         out_degree[prereq_module.course_code] = []

#                     out_degree[prereq_module.course_code].append(current_course_code)

#             in_degree[current_course_code].append(
#                 set(prereq_module.course_code for prereq_module in )
#             )
            
        