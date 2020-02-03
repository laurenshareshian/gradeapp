import sqlite3
import sys
import csv

con = sqlite3.connect("grades.db")
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS grades;")
cur.execute("CREATE TABLE grades "
        "(teacherid INTEGER PRIMARY KEY, Teacher, Class1, Class2, Class3, Class4);")
with open('grades.csv','r') as fin:
	data = csv.reader(fin)  # comma is default delimiter
	next(data, None)  # skip first line
	to_db = []
	for i in data:
		to_db.append ((i[0], i[1], i[2], i[3], i[4])) # do not use first indexing column in csv file
cur.executemany("INSERT INTO grades "
            "(teacher, class1, class2, class3, class4) "
            "VALUES (?, ?, ?, ?, ?);", to_db)
con.commit()
cur.close()
con.close()