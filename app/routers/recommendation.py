"""
Module for operations regarding recommendations in modules2students
"""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from neo4j import Driver
from ..dependencies import get_db_driver  # pylint: disable=import-error
from .models import StudentBase, RecommendationModel
from .recommendation_services import get_recommendations

router = APIRouter(
    prefix="/recommendations", tags=["recommendations"], responses={404: {"description": "Not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/{student_id}", response_model=RecommendationModel)
async def retrieve_recommendations(
    token: Annotated[str, Depends(oauth2_scheme)],
    student_id: str | None = None,
    driver: Driver = Depends(get_db_driver),
) -> RecommendationModel:
    """API endpoint to get a particular student's recommendations"""

    if str is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No student id given"
        )

    return await get_recommendations(student_id, driver, token)
