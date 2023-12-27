"""
Cypher Queries for students
"""

GET_STUDENT = (
    "MATCH (student: Student) "
    "WHERE student.student_id = $student_id "
    "RETURN student.student_id as student_id, student.email as email, "
    "student.first_name as first_name, student.last_name as last_name, "
    "student.major as major, student.disciplines as disciplines, "
    "student.year_of_study as year_of_study"
)

GET_STUDENT_MODULES = (
    "MATCH (s: Student)-[t: TAKES]->(m: Module) "
    "WHERE s.student_id = $student_id "
    "RETURN m.course_code as course_code"
)
