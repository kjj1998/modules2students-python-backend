"""Pydantic models definition.

This package contains the Pydantic model defintiions used for authentication.

"""
from pydantic import BaseModel


class Registration(BaseModel):
    """Model for registration of new users.

    This is a Pydantic model for the registration of new users.

    Attributes:
      student_id:
        The student id is represented as a string.
      password:
        The password is represented as a string.
      email:
        The email is represented as a string.
    """

    student_id: str
    password: str
    email: str


class Authentication(BaseModel):
    """Model to login and authenticate existing users.

    This is a Pydantic model for login of existing users.

    Attributes:
      username:
        The username of the user which is the student id.
      password:
        The password represented as a string.
    """

    username: str
    password: str


class AuthenticationResponse(BaseModel):
    """Model for authentication response of users.

    This is a Pydantic model for the response after authentication of users.

    Attributes:
      access_token:
        The JWT token represented as a string.
      user_id:
        The ID of the user represented as a string.
    """

    access_token: str
    user_id: str
