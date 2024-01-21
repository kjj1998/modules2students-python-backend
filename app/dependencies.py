"""
Dependencies
"""
from . import config  # pylint: disable=import-error
from neo4j import GraphDatabase


async def get_db_driver():
    """Dependency to Neo4j db driver"""

    settings = config.Settings()
    driver = GraphDatabase.driver(
        settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password)
    )
    driver.verify_connectivity()

    try:
        yield driver
    finally:
        driver.close()
