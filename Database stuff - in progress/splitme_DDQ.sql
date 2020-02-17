DROP TABLE IF EXISTS class;
CREATE TABLE class (
    class_id int(11) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    PRIMARY KEY (class_id)
) ENGINGE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS student;
CREATE TABLE student (
    student_id int(11) NOT NULL AUTO_INCREMENT,
    first_name varchar(255) DEFAULT NULL,
    last_name varchar(255) NOT NULL,
    PRIMARY KEY (student_id),
    CONSTRAINT full_name UNIQUE (first_name,last_name)
) ENGINGE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS assignment;
CREATE TABLE assignment (
    assignment_id int(11) NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    class int(11) DEFAULT NULL,
    max_score int(11) DEFAULT NULL,
    PRIMARY KEY (assignment_id),
    FOREIGN KEY (class) REFERENCES class (class_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINGE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS class_student;
CREATE TABLE class_student (
    class int(11) NOT NULL,
    student int(11) NOT NULL,
    FOREIGN KEY (class) REFERENCES class (class_id) ON DELETE CASCADE,
    FOREIGN KEY (student) REFERENCES student (student_id) ON DELETE CASCADE
) ENGINGE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS assignment_student;
CREATE TABLE assignment_student (
    assignment int(11) NOT NULL,
    student int(11) NOT NULL,
    score int(11) DEFAULT NULL,
    FOREIGN KEY (assignment) REFERENCES assignment (assignment_id) ON DELETE CASCADE,
    FOREIGN KEY (student) REFERENCES student (student_id) ON DELETE CASCADE
) ENGINGE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;