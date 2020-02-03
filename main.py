from flask import Flask, render_template
import sqlite3
import sys
import csv
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from config import Config
from flask import flash, redirect

app = Flask(__name__)

bootstrap = Bootstrap(app)

app.config.from_object(Config)


def getClasses(teacherstring):
	con = sqlite3.connect("grades.db")
	molecule = "SELECT * FROM grades WHERE teacher=:teacher"
	cursor = con.execute(molecule, {"teacher": teacherstring})
	rows = cursor.fetchall()
	con.close()
	return rows

@app.route("/about")
def about():
    return render_template("about.html")

class ClassesForm(FlaskForm):
    search = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def search():
    form = ClassesForm()
    noresults = False
    classes = None
    if form.validate_on_submit():
        classes = getClasses(form.search.data.strip())
        if(len(classes)==0):
        	noresults = True     
    return render_template('classesform.html', form=form, classes=classes, noresults=noresults)


if __name__ == "__main__":
    app.run(debug=True)
