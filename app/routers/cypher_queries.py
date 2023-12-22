"""
CRUD Cypher queries for modules
"""

GET_ALL_MODULES = ("MATCH (m:Module) "
        "WITH COUNT(m) AS total "
        "MATCH (m:Module) "
        "RETURN m.course_code AS course_code, m.course_name AS course_name, m.course_info AS course_info, "  # pylint: disable=line-too-long
        "m.faculty AS faculty, m.academic_units AS academic_units, m.broadening_and_deepening AS broadening_and_deepening, m.grade_type AS grade_type, total "  # pylint: disable=line-too-long
        "SKIP $skip LIMIT $limit")

GET_MODULE = ("MATCH (m:Module) "
        "WHERE m.course_code = $course_code "
        "RETURN m.course_code AS course_code, m.course_name AS course_name, m.course_info AS course_info, "  # pylint: disable=line-too-long
        "m.faculty AS faculty, m.academic_units AS academic_units, m.broadening_and_deepening AS broadening_and_deepening, m.grade_type AS grade_type"  # pylint: disable=line-too-long
        )