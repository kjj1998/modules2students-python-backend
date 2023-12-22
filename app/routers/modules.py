"""
Module for operations regarding academic modules in modules2students
"""
from fastapi import APIRouter, Depends
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from . import crud

router = APIRouter(
    prefix="/modules", tags=["modules"], responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_modules(skip: int, limit: int, driver: Driver = Depends(get_db_driver)):
    """API endpoint to read modules data from Neo4j db"""

    modules = crud.get_modules(skip, limit, driver)

    return modules
