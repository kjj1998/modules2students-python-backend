"""
Module for operations regarding students in modules2students
"""
from fastapi import APIRouter, Depends, HTTPException, status
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from . import crud

router = APIRouter(
    prefix="/students", tags=["students"], responses={404: {"description": "Not found"}}
)


@router.get("/{student_id}")
async def read_student(
    student_id: str | None = None, driver: Driver = Depends(get_db_driver)
):
    """API endpoint to get a particular student's information"""

    if str is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No course code given"
        )

    student = crud.get_student(student_id, driver)
    return student
