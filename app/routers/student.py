"""
Module for operations regarding students in modules2students
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from .models import StudentBase
from .student_services import get_student, update_student_details

router = APIRouter(
    prefix="/students", tags=["students"], responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/{student_id}", response_model=StudentBase)
async def read_student(
    token: Annotated[str, Depends(oauth2_scheme)],
    student_id: str | None = None,
    driver: Driver = Depends(get_db_driver),
) -> StudentBase:
    """API endpoint to get a particular student's information."""

    if str is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No student id given"
        )

    student: StudentBase = await get_student(student_id, driver, token)

    return student


@router.put("/", response_model=StudentBase)
async def update_student(
    student: StudentBase,
    token: Annotated[str, Depends(oauth2_scheme)],
    driver: Driver = Depends(get_db_driver)
) -> StudentBase:
    """API endpoint to update a student details."""

    updated_student: StudentBase = await update_student_details(student, driver, token)

    return updated_student
