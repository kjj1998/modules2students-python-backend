"""
Module for operations regarding academic modules in modules2students
"""
from fastapi import APIRouter, Depends
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from . import crud


# URI = "neo4j://localhost:7687"
# AUTH = ("neo4j", "12345678")

router = APIRouter(
    prefix="/modules", tags=["modules"], responses={404: {"description": "Not found"}}
)

# async def get_db_driver():
#     """Dependency to Neo4j db driver"""
#     driver = GraphDatabase.driver(URI, auth=AUTH)
#     driver.verify_connectivity()
#     try:
#         yield driver
#     finally:
#         driver.close()


@router.get("/")
async def read_modules(skip: int, limit: int, driver: Driver = Depends(get_db_driver)):
    """API endpoint to read modules data from Neo4j db"""

    modules = crud.get_modules(skip, limit, driver)

    return modules
