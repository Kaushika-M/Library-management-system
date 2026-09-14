# Library Management System
A simple Library Management System built using **FastAPI, PostgreSQL, SQLAlchemy, HTML and CSS**.

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
- PostgreSQL
- SQLAlchemy
- HTML
- CSS
- Jinja2
- psycopg2

## How to Run
### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary jinja2 python-multipart itsdangerous
```

### 4. Set up PostgreSQL

Make sure PostgreSQL is installed and running.

Create a PostgreSQL database, for example:

```sql
CREATE DATABASE library;
```

### 5. Configure the database

In `database.py`, configure your PostgreSQL connection:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/library"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

Replace `username` and `password` with your PostgreSQL credentials.

### 6. Run the application

```bash
uvicorn main:app --reload
```

### 7. Open in browser

http://127.0.0.1:8000

## Database

This project uses **PostgreSQL** as the database and **SQLAlchemy** as the ORM.

The application connects to PostgreSQL using the `psycopg2` driver.