"""
Cypher queries for recommendations.
"""

GET_CB_MODULES_THAT_FULFILL_PREREQS = (
    "MATCH (s:Student)-[t:TAKES]->(m:Module) " +
    "WHERE s.student_id = $student_id " +
    "MATCH (m)-[sim:SIMILAR]->(rec:Module { community: m.community }) " +
    "WHERE NOT (rec)<-[:MUTUALLY_EXCLUSIVE]->(m) AND sim.score < 0.85 " +
    "MATCH (rec)<-[:ARE_PREREQUISITES]-(prereq_group:PrerequisiteGroup)<-[:INSIDE]-(prereq:Module) " + # pylint: disable=line-too-long
    "MATCH (s:Student)-[t:TAKES]->(prereq:Module) " +
    "WHERE rec.broadening_and_deepening = true " +
    "RETURN rec.course_code AS course_code, rec.course_name AS course_name, rec.course_info AS course_info, " + # pylint: disable=line-too-long
    "rec.faculty AS faculty, rec.academic_units AS academic_units, rec.grade_type AS grade_type, " +
    "rec.broadening_and_deepening AS broadening_and_deepening, sim.score AS score LIMIT 10"
)


GET_CB_MODULES_WITH_NO_PREREQS = (
    "MATCH (s:Student)-[t:TAKES]->(m:Module) " +
    "WHERE s.student_id = $student_id " +
    "MATCH (m)-[sim:SIMILAR]->(rec:Module { community: m.community }) " +
    "WHERE NOT (rec)<-[:MUTUALLY_EXCLUSIVE]->(m) AND sim.score < 0.85 " +
    "AND NOT EXISTS { " +
    "  MATCH (rec)<-[:ARE_PREREQUISITES]-(:PrerequisiteGroup)<-[:INSIDE]-(:Module) " +
    "}" +
    "AND rec.broadening_and_deepening = true " +
    "WITH s, rec, sim " +
    "ORDER BY sim.score DESC " +
    "UNWIND s.disciplines AS disciplines " +
    "MATCH (filteredRec: Module { course_code: rec.course_code}) " +
    "WHERE filteredRec.discipline <> disciplines AND filteredRec.discipline <> 'Interdisciplinary Collaborative Core' " + # pylint: disable=line-too-long
    "AND filteredRec.discipline <> 'CN Yang Scholars Programme' AND filteredRec.discipline <> 'University Scholars Programme' " + # pylint: disable=line-too-long
    "AND filteredRec.discipline <> 'Renaissance Engineering' " +
    "RETURN filteredRec.course_code AS course_code, filteredRec.course_name AS course_name, " +
    "filteredRec.course_info AS course_info, filteredRec.academic_units AS academic_units, " +
    "filteredRec.broadening_and_deepening AS broadening_and_deepening, filteredRec.faculty AS faculty, " + # pylint: disable=line-too-long
    "filteredRec.grade_type AS grade_type, sim.score AS score LIMIT 10"
)


GET_CF_MODULES_THAT_FULFILL_PREREQS = (
    "MATCH (s1:Student)-[r:SIMILAR_TO_USER]->(s2:Student) " +
    "WHERE s1.student_id = $student_id " +
    "WITH s2.student_id AS neighborId, s1, r.jaccard_index AS score " +
    "ORDER BY score DESC, neighborId " +
    "WITH s1, COLLECT(neighborId)[0..10] as neighbours " +
    "UNWIND neighbours AS neighborId " +
    "WITH s1, neighborId " +
    "MATCH (s3:Student)-[:TAKES]->(m:Module) " +
    "WHERE s3.student_id = neighborId AND NOT (s1)-[:TAKES]->(m) " +
    "WITH m AS coursesNotTaken, s1 " +
    "UNWIND s1.disciplines AS disciplines " +
    "WITH coursesNotTaken, disciplines, s1 " +
    "MATCH (coursesNotTakenFiltered:Module { course_code: coursesNotTaken.course_code }) " +
    "WHERE coursesNotTaken.discipline <> disciplines AND coursesNotTaken.discipline <> 'Interdisciplinary Collaborative Core' " + # pylint: disable=line-too-long
    "AND coursesNotTaken.discipline <> 'CN Yang Scholars Programme' AND coursesNotTaken.discipline <> 'University Scholars Programme' " + # pylint: disable=line-too-long
    "WITH DISTINCT coursesNotTakenFiltered, s1 " +
    "MATCH (coursesNotTakenFiltered)<-[:ARE_PREREQUISITES]-(prereq_group:PrerequisiteGroup)<-[:INSIDE]-(prereq:Module) " + # pylint: disable=line-too-long
    "MATCH (s1)-[t:TAKES]->(prereq:Module) " +
    "WITH COUNT(distinct coursesNotTakenFiltered.course_code) AS cnt, coursesNotTakenFiltered " +
    "ORDER BY cnt DESC " +
    "WITH DISTINCT coursesNotTakenFiltered " +
    "RETURN coursesNotTakenFiltered.course_code AS course_code, coursesNotTakenFiltered.course_name AS course_name, " + # pylint: disable=line-too-long
    "coursesNotTakenFiltered.course_info AS course_info, coursesNotTakenFiltered.faculty AS faculty, " + # pylint: disable=line-too-long
    "coursesNotTakenFiltered.academic_units AS academic_units, coursesNotTakenFiltered.grade_type AS grade_type, " + # pylint: disable=line-too-long
    "coursesNotTakenFiltered.broadening_and_deepening AS broadening_and_deepening" # pylint: disable=line-too-long
)


GET_CF_MODULES_WITH_NO_PREREQS = (
    "MATCH (s1:Student)-[r:SIMILAR_TO_USER]->(s2:Student) " +
    "WHERE s1.student_id = $student_id " +
    "WITH s2.student_id AS neighborId, s1, r.jaccard_index AS score " +
    "ORDER BY score DESC, neighborId " +
    "WITH s1, COLLECT(neighborId)[0..10] as neighbours " +
    "UNWIND neighbours AS neighborId " +
    "WITH s1, neighborId " +
    "MATCH (s3:Student)-[:TAKES]->(m:Module) " +
    "WHERE s3.student_id = neighborId AND NOT (s1)-[:TAKES]->(m) " +
    "WITH m AS coursesNotTaken, s1 " +
    "UNWIND s1.disciplines AS disciplines " +
    "WITH coursesNotTaken, disciplines " +
    "MATCH (coursesNotTakenFiltered:Module { course_code: coursesNotTaken.course_code }) " +
    "WHERE coursesNotTaken.discipline <> disciplines AND coursesNotTaken.discipline <> 'Interdisciplinary Collaborative Core' " + # pylint: disable=line-too-long
    "AND coursesNotTaken.discipline <> 'CN Yang Scholars Programme' AND coursesNotTaken.discipline <> 'University Scholars Programme' " + # pylint: disable=line-too-long
    "AND NOT EXISTS { MATCH (coursesNotTaken)<-[:ARE_PREREQUISITES]-(:PrerequisiteGroup)<-[:INSIDE]-(:Module) } " + # pylint: disable=line-too-long
    "WITH COUNT(DISTINCT coursesNotTakenFiltered.course_code) AS cnt, coursesNotTakenFiltered " +
    "ORDER BY cnt DESC " +
    "WITH DISTINCT coursesNotTakenFiltered " +
    "RETURN coursesNotTakenFiltered.course_code AS course_code, coursesNotTakenFiltered.course_name AS course_name, " + # pylint: disable=line-too-long
    "coursesNotTakenFiltered.course_info AS course_info, coursesNotTakenFiltered.faculty AS faculty, " + # pylint: disable=line-too-long
    "coursesNotTakenFiltered.academic_units AS academic_units, coursesNotTakenFiltered.grade_type AS grade_type, " + # pylint: disable=line-too-long
    "coursesNotTakenFiltered.broadening_and_deepening AS broadening_and_deepening" # pylint: disable=line-too-long
)
