"""
CRUD Cypher queries for authentication
"""

REGISTER_USER = (
    "MERGE (s:Student {student_id: $student_id, password: $password, email: $email, " +
    "disciplines: $disciplines, first_name: $first_name, last_name: $last_name, major: $major, " + 
    "year_of_study: $year_of_study })"
)
