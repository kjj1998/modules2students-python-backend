"""
CRUD utility functions for recommendation endpoints.
"""

from collections import deque
from typing import Annotated
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from neo4j import Driver
from jose import JWTError, jwt

import config  # pylint: disable=import-error

from . import db_functions
from .models import StudentBase, ModuleBase, RecommendationModel

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = config.Settings()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_recommendations(
    student_id: str, driver: Driver, token: Annotated[str, Depends(oauth2_scheme)]
) -> RecommendationModel:
    """Retrieve a student's recommendations from the db.

    This function retrieves a student's recommendations from the db
    based on the student id supplied. The function takes in the
    student id, an open instance of the neo4j.Driver and the JWT access
    token.

    Args:
      student_id:
        The id of the student whose information we want to retrieve.
      driver:
        An open instance of the neo4j.Driver.
      token:
        JWT access token.

    Returns:
      The information of the student encapsulated in a RecommendationModel model.
      Raises exceptions if there is an error.
    """
    username: str = ""

    try:
        payload: dict[str, any] = jwt.decode(
            token, settings.secret_key, algorithms=[ALGORITHM]
        )
        username = payload.get("user_id")
        if username is None or username != student_id:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    recs: RecommendationModel = RecommendationModel()

    cb_recs_fulfil_prereq: list[
        ModuleBase
    ] = db_functions.get_cb_recs_that_fulfil_prereq(username, driver)

    cb_recs_no_prereq: list[ModuleBase] = db_functions.get_cb_recs_that_have_no_prereq(
        username, driver
    )

    cf_recs_fulfill_prereq: list[
        ModuleBase
    ] = db_functions.get_cf_recs_that_fulfill_prereq(username, driver)
    cf_recs_no_prereq: list[ModuleBase] = db_functions.get_cf_recs_that_have_no_prereq(
        username, driver
    )

    cb_recs: list[ModuleBase] = cb_recs_no_prereq + cb_recs_fulfil_prereq
    cf_recs: list[ModuleBase] = cf_recs_no_prereq + cf_recs_fulfill_prereq

    cb_recs.sort(key=lambda x: x.score , reverse=True)

    cb_recs_top_10: list[ModuleBase] = cb_recs[:10]
    cf_recs_top_10: list[ModuleBase] = cf_recs[:10]

    recs.cbf_recommendations = cb_recs_top_10
    recs.cf_recommendations = cf_recs_top_10

    return recs
