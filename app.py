import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import bcrypt

# Load environmental variables
load_dotenv()

app = Flask(__name__)

# Use the SQLALCHEMY_DATABASE_URI from the environment
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise
db = SQLAlchemy(app)

class Franchise(db.Model):
    __tablename__ = 'franchises'  # Updated to match the SQL file
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Store(db.Model):
    __tablename__ = 'stores'  # Updated to match the SQL file
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchises.id'), nullable=False)
    branch = db.Column(db.String(100), nullable=False)

    franchise = db.relationship('Franchise', backref='stores')

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    birthday = db.Column(db.Date)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    store = db.relationship('Store', backref='staff')

class Score(db.Model):
    __tablename__ = 'scores'  # Updated to match the SQL file
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    staff = db.relationship('Staff', backref='scores')

@app.route('/signup', methods=['POST'])
def create_staff():
    data = request.get_json()

    # Check if email already exists
    existing_staff = Staff.query.filter_by(email=data['email']).first()
    if existing_staff:
        return jsonify({'message': 'A user with this email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    new_staff = Staff(
        full_name=data['full_name'],
        email=data['email'],
        birthday=data['birthday'],
        store_id=data['store_id'],
        password=hashed_password.decode('utf-8')  # Store the hashed password as a string
    )
    
    db.session.add(new_staff)
    db.session.commit()
    
    return jsonify({'message': 'New staff created'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    staff = Staff.query.filter_by(email=data['email']).first()

    if staff and bcrypt.checkpw(data['password'].encode('utf-8'), staff.password.encode('utf-8')):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)