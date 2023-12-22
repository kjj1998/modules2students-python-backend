"""
Module for operations regarding academic modules in modules2students
"""
from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from . import crud

router = APIRouter(
    prefix="/modules", tags=["modules"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def read_modules(skip: int = 0, limit: int = 10, driver: Driver = Depends(get_db_driver)):
    """API endpoint to read modules data from Neo4j db"""

    modules = crud.get_modules(skip, limit, driver)

    return modules


@router.get("/{course_code}")
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
