from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ClassesForm, StudentForm, AssignmentForm, AddCourseForm
from app.models import User, Student, Assignment, Course
import sqlite3
import sys
import csv

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

courses = []
# eventually we will get these via SQL queries instead
dummycourse1 = Course('Trig')
dummycourse2 = Course('Basket Weaving')
courses.append(dummycourse1)
courses.append(dummycourse2)

@app.route('/')
#@app.route('/index')
#@login_required
def index():
    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### About Tab
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

### Get classes via SQL query
def getClasses(teacherstring):
	con = sqlite3.connect("grades.db")
	molecule = "SELECT * FROM grades WHERE teacher=:teacher"
	cursor = con.execute(molecule, {"teacher": teacherstring})
	rows = cursor.fetchall()
	con.close()
	return rows

### Add Student Form
@app.route('/addmystudent', methods=['GET', 'POST'])
def addStudent():

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    if addStudentForm.validate_on_submit():
    		newstudent = Student(addStudentForm.first.data.strip(), addStudentForm.last.data.strip(), addStudentForm.email.data.strip()) 
	    	students.append(newstudent)
	    	return redirect(url_for('index'))

    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### Add New Student Form
@app.route('/addnewstudent', methods=['GET', 'POST'])
def addNewStudent():

    addStudentForm = StudentForm()
    return render_template('addnewstudent.html', addStudentForm=addStudentForm)

### Save Add Student
@app.route('/saveAddStudent', methods=['POST'])
def saveAddStudent():

    first = request.form['first']
    last = request.form['last']
    email = request.form['email']

    newstudent = Student(first, last, email) 
    students.append(newstudent)      

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)


### Edit Student Form
@app.route('/editstudent/<first>/<last>/<email>', methods=['GET', 'POST'])
def editStudent(first, last, email):
    # replace this for loop with database query eventually to find unique studentID
    for i, student in enumerate(students):
        if student.email == email:
            studentID = i

    editStudentForm = StudentForm()
    return render_template('editstudent.html', editStudentForm=editStudentForm, first=first, last=last, email=email, studentID = studentID)

### Save Student Edits
@app.route('/saveEditStudent/<studentID>', methods=['POST'])
def saveEditStudent(studentID):

    studentID = int(studentID)
    first = request.form['first']
    last = request.form['last']
    email = request.form['email']

    # if the user changed any of these, replace them in database
    if first:
        students[studentID].first = first
    if last:
        students[studentID].last = last
    if email:
        students[studentID].email = email        

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### Delete Student
@app.route('/deleteStudent/<studentID>', methods=['POST'])
def deleteStudent(studentID):

    studentID = int(studentID)
    del students[studentID]

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

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


### Add New Assignment Form
@app.route('/addnewassignment', methods=['GET', 'POST'])
def addNewAssignment():

    addAssignmentForm = AssignmentForm()
    return render_template('addnewassignment.html', addAssignmentForm=addAssignmentForm)

### Save Add Assignment
@app.route('/saveAddAssignment', methods=['POST'])
def saveAddAssignment():

    name = request.form['name']
    date = request.form['date']
    points = request.form['points']

    newassignment = Assignment(name, date, points) 
    assignments.append(newassignment)      

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)


### Edit Assignment Form
@app.route('/editassignment/<name>/<date>/<points>', methods=['GET', 'POST'])
def editAssignment(name, date, points):
    # replace this for loop with database query eventually to find unique assignmentID
    for i, assignment in enumerate(assignments):
        if assignment.name == name:
            assignmentID = i

    editAssignmentForm = AssignmentForm()
    return render_template('editassignment.html', editAssignmentForm=editAssignmentForm, name=name, date=date, points=points, assignmentID=assignmentID)

### Save Assignment Edits
@app.route('/saveEditAssignment/<assignmentID>', methods=['POST'])
def saveEditAssignment(assignmentID):

    assignmentID = int(assignmentID)
    name = request.form['name']
    date = request.form['date']
    points = request.form['points']

    # if the user changed any of these, replace them in database
    if name:
        assignments[assignmentID].name = name
    if date:
        assignments[assignmentID].date = date
    if points:
        assignments[assignmentID].points = points     

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### Delete Assignment
@app.route('/deleteAssigment/<assignmentID>', methods=['POST'])
def deleteAssignment(assignmentID):

    assignmentID = int(assignmentID)
    del assignments[assignmentID]

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()

    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)



### Add Course Form
@app.route('/addcourse', methods=['GET', 'POST'])
def addCourse():

    addCourseForm = AddCourseForm()

    if addCourseForm.validate_on_submit():
    		newcourse = Course(addCourseForm.courseName.data.strip())
	    	courses.append(newcourse)
	    	# anything you print here gets printed to your terminal
	    	print(newcourse.courseName)
    return render_template('addcourse.html', addCourseForm=addCourseForm, courses=courses)
