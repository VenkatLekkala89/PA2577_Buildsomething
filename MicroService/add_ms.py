# address_service.py
from flask import Flask, request, jsonify, flash, url_for, redirect, render_template
from marshmallow import Schema, fields, validate
from flask_sqlalchemy import SQLAlchemy

# Flask application instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Addresses.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


# Address Model
class Addresses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_add = db.Column(db.String(100))
    apartment_num = db.Column(db.Integer)
    pin = db.Column(db.String(10))

    def __init__(self, street_add, apartment_num, pin):
        self.street_add = street_add
        self.apartment_num = apartment_num
        self.pin = pin


@app.route('/')
def show_all():
    return render_template('show_add_all.html', addresses=Addresses.query.all())


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['street_add'] or not request.form['apartment_num'] or not request.form['pin']:
            flash('Please enter all the fields', 'error')
        else:
            address = Addresses(request.form['street_add'], request.form['apartment_num'],
                                request.form['pin'])

            db.session.add(address)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('new_add.html')

@app.route('/query_all')
def query_all():
    return Addresses.query.all()

@app.post('/<int:address_id>/delete/')
def delete(address_id):
    address = Addresses.query.get_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    return redirect(url_for('show_all'))

# # Define a schema for validating data
# class AddressSchema(Schema):
#     address_id = fields.String(required=True, validate=validate.Length(max=50))
#     # Add more fields as needed
#
#
# @app.route('/addresses', methods=['POST'])
# def create_address():
#     try:
#         data = request.get_json()
#         schema = AddressSchema()
#         errors = schema.validate(data)
#         if errors:
#             return jsonify(errors), 400
#         address_id = data['address_id']
#         if address_id in addresses:
#             return "Address already exists", 409
#         addresses[address_id] = data
#         return jsonify(data), 201
#     except KeyError:
#         return "Invalid data or missing 'address_id'", 400
#
#
# @app.route('/addresses/<address_id>', methods=['GET'])
# def get_address(address_id):
#     if address_id in addresses:
#         return jsonify(addresses[address_id])
#     return "Address not found", 404


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    app.run(port=5001, debug=True)
