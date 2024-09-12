import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import bcrypt
from datetime import datetime, timedelta, timezone

import jwt

# Load environmental variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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

class LearningResource(db.Model):
    __tablename__ = 'learning_resources'
    resource_id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(255), nullable=False)  # Resource title
    description = db.Column(db.Text)  # Optional description
    url = db.Column(db.String(255), nullable=False) # URL to the resource

class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    info = db.Column(db.Text, nullable=False)
    followup = db.Column(db.Text, nullable=False)
    fanswer = db.Column(db.Boolean, nullable=False)

def generate_access_token(user_id):
    expiration = datetime.now(tz=timezone.utc) - timedelta(hours=1)
    token = jwt.encode({
        'staff_id': user_id,
        'exp': expiration
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def generate_refresh_token(user_id):
    expiration = datetime.now(tz=timezone.utc) + timedelta(days=30)
    refresh_token = jwt.encode({
        'staff_id': user_id,
        'exp': expiration
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return refresh_token

@app.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data['refresh_token']

    try:
        decoded_refresh_token = jwt.decode(refresh_token, app.config['SECRET_KEY'], algorithms=['HS256'])
        staff_id = decoded_refresh_token['staff_id']

        # If refresh token is valid, generate a new access token
        new_access_token = generate_access_token(staff_id)

        return jsonify({'access_token': new_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

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

@app.route('/api/learning-resources', methods=['GET'])
def get_learning_resources():
    resources = LearningResource.query.all()
    return jsonify([{
        'title': resource.title,
        'description': resource.description,
        'url': resource.url
    } for resource in resources])

@app.route('/api/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([{
        'question': question.question,
        'answer': question.answer,
        'info': question.info,
        'followup': question.followup,
        'fanswer': question.fanswer
    } for question in questions])

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

        access_token = generate_access_token(staff.staff_id)
        refresh_token = generate_refresh_token(staff.staff_id)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@app.route('/add-score', methods=['POST'])
def add_score():
    data = request.get_json()

    if not data['staff_id'] or not data['score']:
        return jsonify({'message': 'Missing data'}), 400

    new_score = Score(
        # date in yyyy-mm-dd hh:mm:ssformat
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        staff_id=data['staff_id'],
        score=data['score']
    )

    db.session.add(new_score)
    db.session.commit()

    return jsonify({'message': 'New score added'}), 201

@app.route('/api/get-scores', methods=['POST'])
def get_scores():
    data = request.get_json()

    if not data or 'staff_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    staff_id = data['staff_id']
    scores = Score.query.filter_by(staff_id=staff_id) \
                        .order_by(Score.date.desc()) \
                        .limit(6) \
                        .all()
    
    # Ensure date is in a string format that the frontend expects
    return jsonify([{
        'score': score.score,
        'date': score.date
    } for score in scores])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)