"""
Module for operations regarding students in modules2students
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from neo4j import Driver

from ..dependencies import get_db_driver
from ..models.student import Student
from ..services.student import get_student, update_student_details

router = APIRouter(
    prefix="/students", tags=["students"], responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/{student_id}", response_model=Student)
async def read_student(
    token: Annotated[str, Depends(oauth2_scheme)],
    student_id: str | None = None,
    driver: Driver = Depends(get_db_driver),
) -> Student:
    """API endpoint to get a particular student's information."""

    if str is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No student id given"
        )

    student: Student = await get_student(student_id, driver, token)

    return student


@router.put("/", response_model=Student)
async def update_student(
    student: Student,
    token: Annotated[str, Depends(oauth2_scheme)],
    driver: Driver = Depends(get_db_driver)
) -> Student:
    """API endpoint to update a student details."""

    updated_student: Student = await update_student_details(student, driver, token)

    return updated_student
