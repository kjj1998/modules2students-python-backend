"""
Cypher Queries for students
"""

GET_STUDENT = (
    "MATCH (student: Student) "
    "WHERE student.student_id = $student_id "
    "RETURN student.student_id as student_id, student.email as email, "
    "student.first_name as first_name, student.last_name as last_name, "
    "student.major as major, student.disciplines as disciplines, "
    "student.year_of_study as year_of_study, student.password as password"
)

GET_STUDENT_MODULES = (
    "MATCH (s: Student)-[t: TAKES]->(m: Module) "
    "WHERE s.student_id = $student_id "
    "RETURN m.course_code AS course_code, m.course_name AS course_name, m.course_info AS course_info, "  # pylint: disable=line-too-long
    "m.faculty AS faculty, m.academic_units AS academic_units, m.broadening_and_deepening AS broadening_and_deepening, m.grade_type AS grade_type"  # pylint: disable=line-too-long
)

UPDATE_STUDENT = (
    "MATCH (s: Student) "
    "WHERE s.student_id = $student_id "
    "SET s.email = $email, s.major = $major, s.first_name = $first_name, "
    "s.last_name = $last_name, s.year_of_study = $year_of_study, s.disciplines = $disciplines "
    "RETURN s.student_id as student_id, s.email as email, "
    "s.first_name as first_name, s.last_name as last_name, "
    "s.major as major, s.disciplines as disciplines, "
    "s.year_of_study as year_of_study"
)

DELETE_MODULE_TAKEN = (
    "MATCH (s:Student { student_id: $student_id })-[r:TAKES]->(m:Module { course_code: $course_code }) " # pylint: disable=line-too-long
    "DELETE r"
)

ADD_MODULE_TAKEN = (
    "MATCH (s:Student { student_id: $student_id }) "
    "MERGE (s)-[:TAKES]->(m:Module { course_code: $course_code }) "
    "RETURN m.course_code AS course_code"
)
