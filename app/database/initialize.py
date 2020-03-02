#!/usr/bin/env python3
import sqlite3

database = "../../../students.db"


# https://www.sqlite.org/datatype3.html

class Student:
    def __init__(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        # Drop if exists
        cur.execute("DROP TABLE IF EXISTS students;")

        # Create
        cur.execute("CREATE TABLE students (student_id INTEGER PRIMARY KEY, first, last, email);")

        # Populate
        to_db = [('John', 'Doe', 'doe@gmail.com'),
                 ('Kanye', 'West', 'west@gmail.com')]

        cur.executemany("INSERT INTO students (first, last, email) VALUES (?, ?, ?);", to_db)

        con.commit()
        cur.close()
        con.close()

class Course:
    def __init__(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        # Drop if exists
        cur.execute("DROP TABLE IF EXISTS class;")

        # Create
        cur.execute("CREATE TABLE class (class_id INTEGER PRIMARY KEY, name TEXT);")

        # Populate
        # Populate
        to_class = [('Algebra I',),
                    ('Algebra II',),
                    ('Differential Calculus',)]

        cur.executemany("INSERT INTO class (name) VALUES (?);", to_class)

        con.commit()
        cur.close()
        con.close()

class Assignment:
    def __init__(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        # Drop if exists
        cur.execute("DROP TABLE IF EXISTS assignment;")

        # Create
        cur.execute("CREATE TABLE assignment (assignment_id INTEGER PRIMARY KEY, name TEXT, date TEXT, class_id INTEGER, max_score INTEGER);")

        # Populate
        # Populate
        to_assignment = [('Syllabus Quiz', 1, 10)]

        cur.executemany("INSERT INTO assignment (name, class_id, max_score) VALUES (?, ?, ?);", to_assignment)

        con.commit()
        cur.close()
        con.close()

class Class_Student:
    def __init__(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        # Drop if exists
        cur.execute("DROP TABLE IF EXISTS class_student;")

        # Create
        cur.execute("CREATE TABLE class_student (cs_id INTEGER PRIMARY KEY, class_id INTEGER, student_id INTEGER);")

        # Populate
        # Populate
        to_cs = [(1, 1)]

        cur.executemany("INSERT INTO class_student (class_id, student_id) VALUES (?, ?);", to_cs)

        con.commit()
        cur.close()
        con.close()

class Assignment_Student:
    def __init__(self, database):
        con = sqlite3.connect(database)
        cur = con.cursor()

        # Drop if exists
        cur.execute("DROP TABLE IF EXISTS assignment_student;")

        # Create
        cur.execute("CREATE TABLE assignment_student (as_id INTEGER PRIMARY KEY, assignment_id INTEGER, student_id INTEGER);")

        # Populate
        # Populate
        to_as = [(1, 1)]

        cur.executemany("INSERT INTO assignment_student (assignment_id, student_id) VALUES (?, ?);", to_as)

        con.commit()
        cur.close()
        con.close()

# Init
Student(database)
Course(database)
Assignment(database)
Class_Student(database)
Assignment_Student(database)