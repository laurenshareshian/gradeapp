-- CLASS OPERATIONS --

-- Create Class --

INSERT INTO class (class.name) VALUES (?);

-- Read Class -- 

SELECT class.class_id as cID, name as name FROM class
ORDER BY cID ASC;

-- Update Class --

UPDATE class SET name=? WHERE class_id=?;

-- Delete Class --

DELETE FROM class WHERE class_id = ?;



-- STUDENT OPERATIONS

-- Create Student --

INSERT INTO student (student.first_name, student.last_name) VALUES (?, ?);

-- Read Student --

SELECT student.student_id as sID, first_name as fname, last_name as lname FROM student
ORDER BY sId ASC;

-- Update Student --

UPDATE student SET first_name=?, last_name=? WHERE student_id=?;

-- Delete Student --

DELETE FROM student WHERE student_id = ?;



-- ASSIGNMENT OPERATIONS --

-- Create Assignment --

INSERT INTO assignment (assignment.name, assignment.class, assignment.max_score) VALUES (?, ?, ?);

-- Read Assignment --

SELECT assignment.assignment_id as aID, name as name, class.name as class, max_score as max_score FROM assignment
LEFT JOIN class ON assignment.class = class.class_id
ORDER BY aID ASC;

-- Update Assignment --

UPDATE assignment SET name=?, class=?, max_score=? WHERE assignment_id=?;

-- Delete Assignment --

DELETE FROM assignment WHERE assignment_id=?;



-- CLASS_STUDENT OPERATIONS --

-- Create Class_Student --

INSERT INTO class_student (class_student.class, class_student.student) VALUES (?, ?);

-- Read Class_Student --

SELECT class.name as className, student.first_name as studentFname, student.last_name as studentLname FROM class_student
LEFT JOIN class ON class_student.class = class.class_id
LEFT JOIN student on class_student.student = student.student_id
WHERE class_student.class = ?;

-- Update Class_Student --

-- Delete Class_Student --

DELETE FROM class_student WHERE class_student.class = ? AND class_student.student = ?



-- ASSIGNMENT_STUDENT OPERATIONS --

-- Create Assignment_Student --

INSERT INTO assignment_student (assignment_student.assignment, assignment_student.student, assignment_student.score) VALUES (?, ?, ?);

-- Read Assignment_Student --

SELECT student.first_name as studentFname, student.last_name as studentLname, score as score, assignment.max_score as max_score FROM assignment_student
LEFT JOIN student ON assignment_student.student = student.student_id
LEFT JOIN assignment ON assignment_student.assignment = assignment.assignment_id
WHERE assignment_student.assignment = ? AND assignment.class = ?;

-- Update Assignment_Student --

UPDATE assignment_student SET score = ? WHERE assignment = ? AND student = ?;

-- Delete Assignment_Student --

DELETE FROM assignment_student WHERE assignment = ? AND student = ?;
