# SoftwareSathi Assignment

## Overview

**SoftwareSathi** is a Django-based web application that provides an API for managing user authentication, registration, login, and data management. The project aims to facilitate easy and secure user management through well-documented API endpoints.

## Features

- **User Signup**: Allows users to create an account with username, email, and password.
- **User Login**: Provides a secure login mechanism with JWT token generation.
- **Data Management**: Supports CRUD operations for managing data entries.
- **User Details**: Retrieves, updates, and deletes user information.

## Installation

1. Navigate to the project folder:
    ```bash
    cd SoftwareSathi

2. Create a virtual environment:

    python -m venv venv

3. Activate the virtual environment:
    * On Windows:
        venv\Scripts\activate

    * On macOS/Linux:
        source venv/bin/activate

4. Install dependencies:

    pip install -r requirements.txt

5. Apply database migrations:

    python manage.py migrate

6. Run the development server:

    python manage.py runserver

Your application should now be running at http://127.0.0.1:8000/

# API Endpoints
## User Signup

POST api/auth/signup/
Creates a new user.

Request Example:

{
  "username": "user1",
  "email": "user1@example.com",
  "password": "securepassword"
}

Response Example:

{
  "message": "User created successfully",
  "user_id": 1
}

## User Login

POST /api/login
Logs in an existing user.

Request Example:

{
  "email": "user1@example.com",
  "password": "securepassword"
}

Response Example:

{
  "message": "Login successful",
  "token": "jwt_token_here"
}

## Data Creation
POST /api/data
Creates a new data entry.

Request Example:

{
  "title": "Data title",
  "description": "Description of the data"
}

Response Example:

{
  "title": "Data title",
  "description": "Description of the data"
}


## API Endpoints
POST /api/auth/signup - User Signup

POST /api/auth/login - User Login

GET /api/users - List Users (Admin)

GET /api/users/<id> - Retrieve User

PUT /api/users/<id> - Update User

DELETE /api/users/<id> - Delete User

POST /api/data - Create Data

GET /api/data - List Data

PUT /api/data/<id> - Update Data

DELETE /api/data/<id> - Delete Data