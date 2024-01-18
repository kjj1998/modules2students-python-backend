"""
Constants
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """App Constants"""

    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    secret_key: str

    model_config = SettingsConfigDict(env_file="../.env")
