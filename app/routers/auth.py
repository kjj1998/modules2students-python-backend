"""API endpoints for authentication operations

This module contains the various API endpoints for authentication operations.

"""
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from neo4j import Driver
from dependencies import get_db_driver  # pylint: disable=import-error
from .auth_services import register, authenticate_user
from .models import RegistrationModel, AuthenticationResponseModel, AuthenticationModel

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=AuthenticationResponseModel)
async def register_user(
    registration: RegistrationModel, driver: Driver = Depends(get_db_driver)
) -> AuthenticationResponseModel:
    """API endpoint to register a new user."""

    return register(registration, driver)


@router.post("/login", response_model=AuthenticationResponseModel)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    driver: Driver = Depends(get_db_driver)
) -> AuthenticationResponseModel:
    """API endpoint to login and authenticate existing users."""

    login_details: AuthenticationModel = AuthenticationModel(
        username=form_data.username,
        password=form_data.password
    )

    return authenticate_user(login_details, driver)
