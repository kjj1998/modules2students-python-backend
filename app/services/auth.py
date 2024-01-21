"""Authentication functions."""

from datetime import datetime, timedelta, timezone
from neo4j import Driver
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from .. import config
from ..database import auth_db, student_db
from ..models.auth import AuthenticationResponse, Registration, Authentication
from ..models.student import Student, StudentDB

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = config.Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
hash_key = settings.secret_key
access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def verify_password(plain_password, hashed_password) -> bool:
    """Verify that the password given is the same as the hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    """Get the bcrypt hash of the given password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Function to create JWT access token."""
    to_encode: dict = {"user_id": data.student_id}

    if expires_delta:
        expire: datetime = datetime.now(timezone.utc) + expires_delta
    else:
        expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, hash_key, algorithm=ALGORITHM)

    return encoded_jwt


def register(
    registeration_details: Registration, driver: Driver
) -> AuthenticationResponse:
    """Register a user

    Register a user using the credentials supplied in the RegistrationModel
    provided.

    Args:
      register:
        The RegistrationModel containing the credentials to be used in the
        registration process.
      driver:
        An open instance of the neo4j Driver.

    Returns:
      The AuthenticationResponseModel after registration.
    """

    if student_db.get_student(registeration_details.student_id, driver) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student with id ${registeration_details.student_id} already exists!",
        )

    new_student: Student = Student(
        student_id=registeration_details.student_id,
        email=registeration_details.email,
    )

    hashed_password = get_password_hash(registeration_details.password)
    auth_db.register_student(new_student, hashed_password, driver)

    access_token = create_access_token(new_student, access_token_expires)

    return AuthenticationResponse(
        access_token=access_token, user_id=registeration_details.student_id
    )


def authenticate_user(
    authenticate_details: Authentication, driver: Driver
) -> AuthenticationResponse:
    """Authtenticate existing users."""

    student: StudentDB = student_db.get_student(
        authenticate_details.username, driver
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with id ${authenticate_details.student_id} does not exist!",
        )

    if not verify_password(authenticate_details.password, student.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password!",
        )

    access_token = create_access_token(student, access_token_expires)

    return AuthenticationResponse(
        access_token=access_token, user_id=authenticate_details.username
    )
