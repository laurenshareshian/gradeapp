import sqlite3
import sys
import csv

con = sqlite3.connect("students.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS students;")
cur.execute("CREATE TABLE students "
        "(studentid INTEGER PRIMARY KEY, first, last, email);")
to_db = [('John', 'Doe', 'doe@gmail.com'), ('Kanye', 'West', 'west@gmail.com')]
cur.executemany("INSERT INTO students "
            "(first, last, email) "
            "VALUES (?, ?, ?);", to_db)
con.commit()
cur.close()
con.close()