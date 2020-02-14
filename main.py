from flask import Flask, render_template
import sqlite3
import sys
import csv
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from config import Config
from flask import flash, redirect,  url_for

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config.from_object(Config)


### About Tab
@app.route("/about")
def about():
    return render_template("about.html")

### Get classes via SQL query
def getClasses(teacherstring):
	con = sqlite3.connect("grades.db")
	molecule = "SELECT * FROM grades WHERE teacher=:teacher"
	cursor = con.execute(molecule, {"teacher": teacherstring})
	rows = cursor.fetchall()
	con.close()
	return rows

### Create Classes Form
class ClassesForm(FlaskForm):
    teachername = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')

### Renders View Classes Page
@app.route('/classes', methods=['GET', 'POST'])
def displayClasses():
    form = ClassesForm()
    noresults = False ## keeps track of if SQL query returned results or not
    classes = None  ## this variable will hold classes obtained from SQL query
    if form.validate_on_submit():
        classes = getClasses(form.teachername.data.strip())
        if(len(classes)==0):
        	noresults = True     
    return render_template('classesform.html', form=form, classes=classes, noresults=noresults)


#### Add Student Form
class StudentForm(FlaskForm):
    first = StringField('First', validators=[DataRequired()])
    last = StringField('Last', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit1 = SubmitField('Submit')

### Create Student Object
class Student:
  def __init__(self, first, last, email):
    self.first = first
    self.last = last
    self.email = email

#### Add Assignment Form
class AssignmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    points = StringField('Points', validators=[DataRequired()])
    submit2 = SubmitField('Submit')

# create Assignment object
class Assignment:
  def __init__(self, name, date, points):
    self.name = name
    self.date = date
    self.points = points


# initialize students and arrays
students = []
# eventually we will get these via SQL queries instead
dummystudent1 = Student('John', 'Doe', 'doe@gmail.com')
dummystudent2 = Student('Kanye', 'West', 'west@gmail.com')
students.append(dummystudent1)
students.append(dummystudent2)

assignments = []
# eventually we will get these via SQL queries instead
dummyassignment1 = Assignment('HW 1', '01-01-2020', 5)
dummyassignment2 = Assignment('HW 2', '01-02-2020', 10)
assignments.append(dummyassignment1)
assignments.append(dummyassignment2)


### this is the main page that contains both forms
@app.route('/')
def index():
    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### Add Student Form
@app.route('/addmystudent', methods=['GET', 'POST'])
def addStudent():

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    if addStudentForm.validate_on_submit():
    		newstudent = Student(addStudentForm.first.data.strip(), addStudentForm.last.data.strip(), addStudentForm.email.data.strip()) 
	    	students.append(newstudent)
	    	# anything you print here gets printed to your terminal
	    	print(newstudent.first, newstudent.last, newstudent.email)
	    	return redirect(url_for('index'))
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### Add Assignment Form
@app.route('/addmyassignment', methods=['GET', 'POST'])
def addAssignment():

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    if addAssignmentForm.validate_on_submit():
    		newassignment = Assignment(addAssignmentForm.name.data.strip(), addAssignmentForm.date.data.strip(), addAssignmentForm.points.data.strip()) 
	    	assignments.append(newassignment)
	    	# anything you print here gets printed to your terminal
	    	print(newassignment.name, newassignment.date, newassignment.points)
	    	return redirect(url_for('index'))
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)


if __name__ == "__main__":
    app.run(debug=True)
