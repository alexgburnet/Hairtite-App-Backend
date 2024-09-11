# Hairtite App Backend

This repository contains the backend code for the Hairtite app, built with Flask and SQLAlchemy. The backend handles authentication, data management, and interaction with a PostgreSQL database.

## Overview

The Hairtite app backend provides several API endpoints for user management, data retrieval, and operations related to franchises, stores, staff, and scores.

## Features

- Authentication: User sign-up, login, and token-based authentication with JWT.
- Data Retrieval: Endpoints for fetching countries, companies, branches, learning resources, and questions.
- Data Operations: Add staff, update scores, and query recent scores.

## Setup

### Database

<p align="center">
  <img src="https://github.com/alexgburnet/Hairtite-App-Backend/blob/main/Assets/Entity-Relationship%20Diagram.png" alt="Diagram for database" width="500"/>
</p>

see init.sql for the database. Make sure to uncomment the code for the permissions, and change the name to your user

### Prerequisites

	•	Python 3.7 or higher
	•	PostgreSQL
	•	pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/alexgburnet/Hairtite-App-Backend.git
cd Hairtite-App-Backend
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a .env file

Create a .env file in the root directory and add the following environment variables:

```env
SECRET_KEY=your_secret_key
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=your_database_host
DATABASE_NAME=your_database_name
```

4. Set up the database

Ensure you have PostgreSQL running and create the required database. You can use the provided init.SQL schema to set up the tables and add the correct permissions

5. Run the application

```bash
python app.py
```

The app will be accessible at `http://localhost:3000`

## API Endpoints

### Authentication

- Sign Up

POST /signup
Request Body:
```json
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "password": "your_password",
  "birthday": "dd/mm/yyyy",
  "store_id": 1
}
```

- Login

POST /login
Request Body:
```json
{
  "email": "john.doe@example.com",
  "password": "your_password"
}
```

Response: 
```json
{
  "access_token": "your_access_token",
  "refresh_token": "your_refresh_token"
}
```

- Refresh Token
POST /refresh
Request Body:
```json
{
  "refresh_token": "your_refresh_token"
}
```

Response:
```json
{
  "access_token": "new_access_token"
}
```


### Data Retrieval

- Get Countries
GET /api/countries
Response:
```json
["United States", "United Kingdom", "Canada", "Australia", "Germany"]
```

- Get Companies
GET /api/companies?country=country_name
Response:
```json
["McDonalds", "Starbucks", "Subway"]
```

- Get Branches
GET /api/branches?country=country_name&company=company_name
Response:
```json
["Branch 1", "Branch 2", "Branch 3"]
```

- Get Learning Resources
GET /api/learning-resources
Response: 
```json
[
  {
    "title": "Resource Title",
    "description": "Resource Description",
    "url": "http://example.com"
  }
]
```

- Get Questions
GET /api/questions
Response:
```json
[
  {
    "question": "Question text",
    "answer": true,
    "info": "Additional info",
    "followup": "Follow-up text",
    "fanswer": false
  }
]
```

### Data Operations

- Add Score
POST /add-score
Request Body:
```json
{
  "staff_id": 1,
  "score": 85
}
```
Response:
```json
{
  "message": "New score added"
}
```

- Get Scores
POST /api/get-scores
Request Body:
```json
{
  "staff_id": 1
}
```

Response:
```json
[
  {
    "score": 85,
    "date": "2024-09-01 10:00:00"
  }
]
```