"""
CRUD Cypher queries for modules
"""

GET_ALL_MODULES = (
        "MATCH (m:Module) "
        "WITH COUNT(m) AS total "
        "MATCH (m:Module) "
        "RETURN m.course_code AS course_code, m.course_name AS course_name, m.course_info AS course_info, "  # pylint: disable=line-too-long
        "m.faculty AS faculty, m.academic_units AS academic_units, m.broadening_and_deepening AS broadening_and_deepening, m.grade_type AS grade_type, total "  # pylint: disable=line-too-long
        "SKIP $skip LIMIT $limit"
        )

GET_MODULE = (
        "MATCH (m:Module) "
        "WHERE m.course_code = $course_code "
        "RETURN m.course_code AS course_code, m.course_name AS course_name, m.course_info AS course_info, "  # pylint: disable=line-too-long
        "m.faculty AS faculty, m.academic_units AS academic_units, m.broadening_and_deepening AS broadening_and_deepening, m.grade_type AS grade_type"  # pylint: disable=line-too-long
        )

SEARCH_MODULES = (
        "CALL db.index.fulltext.queryNodes('moduleIndex', $search_term) YIELD node, score " +
        "WITH COUNT(*) AS total " +
        "CALL db.index.fulltext.queryNodes('moduleIndex', $search_term) YIELD node, score " +
        "RETURN node.course_code AS course_code, node.course_name AS course_name, " +
        "node.course_info AS course_info, node.academic_units AS academic_units, " +
        "node.faculty AS faculty, node.grade_type AS grade_type, " +
        "node.broadening_and_deepening AS broadening_and_deepening, " +
        " score, total " +
        "SKIP $skip LIMIT $limit"
        )

GET_MODULES_COURSE_CODES = (
        "MATCH (m:Module) " +
        "RETURN m.course_code AS course_code"
        )

GET_FACULTIES = (
        "MATCH (m:Module) " +
        "WITH m.faculty AS faculty " +
        "RETURN DISTINCT faculty"
        )

GET_MODULES_FOR_A_FACULTY = (
        "MATCH (m:Module) " +
        "WHERE m.faculty = $faculty " +
        "RETURN m.course_code AS course_code, m.course_name AS course_name"
        )
