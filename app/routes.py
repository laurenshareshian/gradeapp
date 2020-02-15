from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ClassesForm, StudentForm, AssignmentForm
from app.models import User, Student, Assignment
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

### Renders View Classes Page
@app.route('/classes', methods=['GET', 'POST'])
def displayClasses():
    form = ClassesForm()
    noresults = False ## keeps track of if SQL query returned results or not
    classes = []  ## this variable will hold classes obtained from SQL query
    teacher = None
    if form.validate_on_submit():
        # classes = getClasses(form.teachername.data.strip()) # use dummy data for now
        teacher = form.teachername.data.strip()
        classes = ['Algebra', 'Geometry', 'Calculus']
        if(len(classes)==0):
        	noresults = True     
    return render_template('classesform.html', form=form, teacher=teacher, classes=classes, noresults=noresults)


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
