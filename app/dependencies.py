"""
Dependencies
"""
from neo4j import GraphDatabase

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "12345678")

async def get_db_driver():
    """Dependency to Neo4j db driver"""
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    try:
        yield driver
    finally:
        driver.close()
