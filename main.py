import re
from flask import *
from flask import request
from flask import render_template
from flask import url_for 
from flask_sqlalchemy import SQLAlchemy
import flask_sqlalchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///employees.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="randomkey"

db=SQLAlchemy(app)

class Employees(db.Model):
    id=db.Column('employee_id',db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    salary=db.Column(db.Integer)
    age=db.Column(db.Integer)

    def __init__(self,name,salary,age):
        self.name=name
        self.salary=salary
        self.age=age


@app.route('/')

def list():
    return render_template('home.html',Employees=Employees.query.all())

@app.route('/add',methods=['GET','POST'])

def add():
    if request.method=='POST':

        if not request.form['name'] or not request.form['salary'] or not request.form['age'] :
            flash("please fill the input vlaues correctly")
        
        else:

            employee=Employees(request.form['name'],request.form['salary'] ,request.form['age'])

            db.session.add(employee)
            db.session.commit()
            flash("record added successfulyy")
            return redirect(url_for('list'))
    return render_template('add.html')

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)