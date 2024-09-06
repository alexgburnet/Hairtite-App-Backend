import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

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

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    birthday = db.Column(db.Date)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    store = db.relationship('Store', backref='staff')

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    franchise_id = db.Column(db.Integer, db.ForeignKey('franchises.id'), nullable=False)
    branch = db.Column(db.String(100), nullable=False)

    franchise = db.relationship('Franchise', backref='stores')

class Franchise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    staff = db.relationship('Staff', backref='scores')

if __name__ == '__main__':
    app.run(debug=True)