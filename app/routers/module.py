"""API endpoints for operations regarding modules

This module contains the various API endpoints for modules operations.

"""
from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from .models import ModuleBase, ModuleCourseCodeAndName
from .module_services import (
    get_modules,
    search_modules,
    get_modules_course_codes,
    get_module,
    get_faculties, 
    get_modules_in_a_faculty,
    get_total_number_of_modules
)

router = APIRouter(
    prefix="/modules", tags=["modules"], responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[ModuleBase])
async def read_modules(
    skip: int = 0,
    limit: int = 10,
    driver: Driver = Depends(get_db_driver)
) -> list[ModuleBase]:
    """API endpoint to read modules data from the db.
    
    """

    modules = get_modules(skip, limit, driver)

    return modules


@router.get("/{course-code}", response_model=ModuleBase)
async def read_module(
    course_code: str | None = None, driver: Driver = Depends(get_db_driver)
) -> ModuleBase:
    """API endpoint to read a single module from the db.
    
    """

    if str is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No course code given"
        )
    module = get_module(course_code, driver)
    if module is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Module with course code {course_code} is not found",
        )

    return module


@router.get("/search/{search-term}", response_model=list[ModuleBase])
async def search(
    search_term: str,
    skip: int = 0,
    limit: int = 10,
    driver: Driver = Depends(get_db_driver),
) -> list[ModuleBase]:
    """API endpoint to search for relevant modules based on a search term.
    
    """

    modules = search_modules(search_term, skip, limit, driver)

    return modules


@router.get("/get/course-codes", response_model=list[str])
async def retrieve_course_codes(driver: Driver = Depends(get_db_driver)) -> list[str]:
    """API endpoint to get all modules' course codes.
    
    """

    course_codes = get_modules_course_codes(driver)

    return course_codes


@router.get("/get/faculties", response_model=list[str])
async def retrieve_faculties(driver: Driver = Depends(get_db_driver)) -> list[str]:
    """API endpoint to get all faculties.
    
    """

    faculties = get_faculties(driver)

    return faculties


@router.get("/faculty/{faculty}", response_model=list[ModuleCourseCodeAndName])
async def retrieve_all_modules_in_a_faculty(
    faculty: str, driver: Driver = Depends(get_db_driver)
) -> list[ModuleCourseCodeAndName]:
    """API endpoint to get all modules in a faculty.
    
    """

    modules = get_modules_in_a_faculty(faculty, driver)

    return modules

@router.get("/get/number-of-modules")
async def retrieve_total_number_of_modules(driver: Driver = Depends(get_db_driver)) -> int:
    """API endpoint to get total number of modules.
    
    """

    return get_total_number_of_modules(driver)
