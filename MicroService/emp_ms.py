# employee_service.py
from flask import Flask, request, jsonify, flash, url_for, redirect, render_template
from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy

# Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Employees.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


# employees = {}

# Employee Model
class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(50))
    doj = db.Column(db.String(10))

    def __init__(self, name, location, doj):
        self.name = name
        self.location = location
        self.doj = doj


@app.route('/')
def show_all():
    return render_template('show_emp_all.html', employees=Employees.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['location'] or not request.form['doj']:
            flash('Please enter all the fields', 'error')
        else:
            employee = Employees(request.form['name'], request.form['location'],
                                 request.form['doj'])

            db.session.add(employee)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new_emp.html')


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(port=5000, debug=True)
