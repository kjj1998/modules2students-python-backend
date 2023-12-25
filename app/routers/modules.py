"""
Module for operations regarding academic modules in modules2students
"""
from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from . import crud, models

router = APIRouter(
    prefix="/modules", tags=["modules"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[models.ModuleBase])
async def read_modules(
    skip: int = 0, limit: int = 10, driver: Driver = Depends(get_db_driver)
):
    """API endpoint to read modules data from Neo4j db"""

    modules = crud.get_modules(skip, limit, driver)

    return modules


@router.get("/{course_code}", response_model=models.ModuleBase)
async def read_module(
    course_code: str | None = None, driver: Driver = Depends(get_db_driver)
):
    """API endpoint to read a single module from the db"""

    if str is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No course code given"
        )
    module = crud.get_module(course_code, driver)
    if module is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with course code {course_code} is not found",
        )

    return module


@router.get("/search/{search_term}", response_model=list[models.ModuleBase])
async def search(
    search_term: str,
    skip: int = 0,
    limit: int = 10,
    driver: Driver = Depends(get_db_driver),
):
    """API endpoint to search for relevant modules based on a search term"""

    modules = crud.search_modules(search_term, skip, limit, driver)

    return modules


@router.get("/get/coursecodes", response_model=list[str])
async def retrieve_course_codes(driver: Driver = Depends(get_db_driver)):
    """API endpoint to get all modules' course codes"""

    course_codes = crud.get_modules_course_codes(driver)

    return course_codes


@router.get("/get/faculties", response_model=list[str])
async def retrieve_faculties(driver: Driver = Depends(get_db_driver)):
    """API endpoint to get all faculties"""

    faculties = crud.get_faculties(driver)

    return faculties

@router.get("/faculty/{faculty}", response_model=list[models.ModuleCourseCodeAndName])
async def retrieve_all_modules_in_a_faculty(faculty: str, driver: Driver = Depends(get_db_driver)):
    """API endpoint to get all modules in a faculty"""

    modules = crud.get_modules_in_a_faculty(faculty, driver)

    return modules
