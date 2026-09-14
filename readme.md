A simple Library Management System built using **FastAPI, SQLite, SQLAlchemy, HTML and CSS**.

## Features

- Student Signup and Login
- Search Books
- View All Books
- Add Books
- Issue Books
- Return Books
- View My Borrowed Books
- Logout

## Technologies Used

- Python
- FastAPI
- SQLite
- SQLAlchemy
- HTML
- CSS
- Jinja2

## How to Run

### 1. Create virtual environment

python -m venv venv

### 2. Activate it

venv\Scripts\activate

### 3. Install dependencies

pip install fastapi uvicorn sqlalchemy jinja2 python-multipart itsdangerous

### 4. Run the application

uvicorn main:app --reload

### 5. Open in browser

http://127.0.0.1:8000
