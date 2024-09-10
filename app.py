import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import bcrypt
from datetime import datetime

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
    __tablename__ = 'franchises'
    franchise_id = db.Column(db.Integer, primary_key=True)  # Adjusted to match the SQL schema
    name = db.Column(db.String(255), unique=True, nullable=False)

    stores = db.relationship('Store', backref='franchise', lazy=True)  # Added reverse relationship

class Store(db.Model):
    __tablename__ = 'stores'
    store_id = db.Column(db.Integer, primary_key=True)  # Adjusted to match the SQL schema
    country = db.Column(db.String(100), nullable=False)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchises.franchise_id'), nullable=False)  # Adjusted foreign key reference
    branch = db.Column(db.String(100), nullable=False)

    staff = db.relationship('Staff', backref='store', lazy=True)  # Added reverse relationship for staff

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)  # Adjusted to match the SQL schema
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    birthday = db.Column(db.Date)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)  # Adjusted foreign key reference
    password = db.Column(db.String(255), nullable=False)

    scores = db.relationship('Score', backref='staff', lazy=True)  # Added reverse relationship for scores

class Score(db.Model):
    __tablename__ = 'scores'
    score_id = db.Column(db.Integer, primary_key=True)  # Adjusted to match the SQL schema
    date = db.Column(db.DateTime, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=False)  # Adjusted foreign key reference
    score = db.Column(db.Integer, nullable=False)

@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = db.session.query(Store.country).distinct().all()
    return jsonify([country[0] for country in countries])

@app.route('/api/companies', methods=['GET'])
def get_companies():
    country = request.args.get('country')  # Use request.args for GET requests

    if not country:
        return jsonify({'error': 'Country parameter is required'}), 400

    # Query to get distinct franchise names based on the country
    companies = db.session.query(Franchise.name) \
                          .join(Store) \
                          .filter(Store.country == country) \
                          .distinct() \
                          .all()

    return jsonify([company[0] for company in companies])

@app.route('/api/branches', methods=['GET'])
def get_branches():
    country = request.args.get('country')
    company = request.args.get('company')

    if not country or not company:
        return jsonify({'error': 'Both country and company parameters are required'}), 400

    # Query to get distinct branches based on country and company
    branches = db.session.query(Store.branch) \
                         .join(Franchise) \
                         .filter(Store.country == country, Franchise.name == company) \
                         .distinct() \
                         .all()

    return jsonify([branch[0] for branch in branches])


@app.route('/get-store-id', methods=['POST'])
def get_store_id():
    data = request.get_json()
    
    country = data['country']
    franchise_name = data['company']
    branch = data['branch']
    
    # Get the franchise ID from the franchise name
    franchise = Franchise.query.filter_by(name=franchise_name).first()
    if not franchise:
        return jsonify({'message': 'Franchise not found'})

    # Query the store based on country, franchise ID, and branch
    store = Store.query.filter_by(
        country=country,
        franchise_id=franchise.franchise_id,  # Use franchise_id here, not franchise
        branch=branch
    ).first()

    if not store or store == 'None':
        return jsonify({'message': 'Store not found'})

    return jsonify({'store_id': store.store_id})

@app.route('/signup', methods=['POST'])
def create_staff():
    data = request.get_json()

    if not data['full_name'] or not data['email'] or not data['password'] or not data['birthday'] or not data['store_id']:
        return jsonify({'message': 'Missing data'}), 400

    # Check if email already exists
    existing_staff = Staff.query.filter_by(email=data['email']).first()
    if existing_staff:
        return jsonify({'message': 'A user with this email already exists'}), 409   # 409 Conflict

    # Hash the password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    birthday = datetime.strptime(data['birthday'], '%d/%m/%Y')

    formated_birthday = datetime.strftime(birthday, '%Y-%m-%d')

    new_staff = Staff(
        full_name=data['full_name'],
        email=data['email'],
        birthday=formated_birthday,
        store_id=data['store_id'],
        password=hashed_password.decode('utf-8')  # Store the hashed password as a string
    )
    
    db.session.add(new_staff)
    db.session.commit()
    
    return jsonify({'message': 'New staff created'}), 201 # 201 Created

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