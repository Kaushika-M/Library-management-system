from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,RedirectResponse
from  fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.models import Student,Book ,Borrow,Base
from app.database import SessionLocal 
from starlette.middleware.sessions import SessionMiddleware
from app.database import engine
Base.metadata.create_all(bind=engine)
templates=Jinja2Templates(directory="app/templates")
from sqlalchemy import func
from datetime import datetime
from fastapi.staticfiles import StaticFiles

app=FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="my-secret-key"
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse(
            "index.html",
            {"request": request}
    )

@app.get("/login",response_class=HTMLResponse)
def login(request:Request):
    return templates.TemplateResponse("login.html",
                                      {"request":request} 
                                      )

@app.post("/login")
def loginP(request:Request,
           email:str= Form(...),
           password:str= Form(...)):
    db=SessionLocal()
    stu=db.query(Student).filter(Student.email==email).first()

    if not stu or stu.password!=password:
        db.close()
        return templates.TemplateResponse("login.html",
               {"request":request,"error":"Invalid email/password"})
    request.session["student_id"] = stu.id
    db.close()    
    return RedirectResponse(url="/",status_code=303)    

@app.get("/signup",response_class=HTMLResponse)
def signup(request:Request):
    return templates.TemplateResponse("signup.html",
                                      {"request":request}
                                      )

@app.post("/signup")
def signup(request: Request,
    name:str=Form(...),       
    email: str = Form(...),
    password: str = Form(...),
    confirm: str = Form(...)
):
    if password != confirm:
        return "Passwords do not match"

    db = SessionLocal()

    # Check if email already exists
    existing = db.query(Student).filter(
        Student.email == email
    ).first()

    if existing:
        db.close()
        return "Email already registered"

    # Create student
    st = Student()
    st.email = email
    st.password = password

    db.add(st)
    db.commit()
    db.close()

    return RedirectResponse(
        url="/login",
        status_code=303
    )

@app.get("/search",response_class=HTMLResponse)
def search(request:Request):
    return templates.TemplateResponse("search.html",
                                      {"request":request})

@app.post("/search")
def search(request:Request,
           title:str=Form(...)):
    db=SessionLocal()
    book=db.query(Book).filter(func.lower(Book.title)==title.lower()).first()
    if book is None or book.available==False: 
        db.close()
        return "No such Books available."
    db.close()
    return templates.TemplateResponse("search.html",
                                      {"request":request,
                                       "book":book})

@app.post("/issue")
def issue_book(request: Request, id: int = Form(...)):
    student_id = request.session.get("student_id")

    if student_id is None:
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    book = db.query(Book).filter(Book.id == id).first()

    if book is None:
        db.close()
        return "Book not found"

    if not book.available:
        db.close()
        return "Book is already borrowed"

    borrow = Borrow()
    borrow.book_id = id
    borrow.stud_id = student_id
    borrow.borrow_date = datetime.now()

    db.add(borrow)

    book.available = False

    db.commit()
    db.close()

    return "Book issued successfully"

@app.get("/payment/{borrow_id}", response_class=HTMLResponse)
def payment(request: Request, borrow_id: int):

    db = SessionLocal()

    borrow = db.query(Borrow).filter(
        Borrow.id == borrow_id
    ).first()

    if borrow is None:
        db.close()
        return "Borrow record not found"

    db.close()

    return templates.TemplateResponse(
        "payment.html",
        {
            "request": request,
            "borrow": borrow
        }
    )

@app.post("/payment/{borrow_id}")
def make_payment(request: Request, borrow_id: int):

    student_id = request.session.get("student_id")

    if student_id is None:
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    borrow = db.query(Borrow).filter(
        Borrow.id == borrow_id,
        Borrow.stud_id == student_id
    ).first()

    if borrow is None:
        db.close()
        return "Borrow record not found"

    book = db.query(Book).filter(
        Book.id == borrow.book_id
    ).first()

    if book is None:
        db.close()
        return "Book not found"

    # Mark fine as paid
    borrow.paid = True

    # Make the book available again
    book.available = True

    db.commit()
    db.close()

    return RedirectResponse(
        url="/mybooks",
        status_code=303
    )

@app.post("/return")
def return_book(request: Request, book_id: int = Form(...)):

    student_id = request.session.get("student_id")

    if student_id is None:
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    borrow = db.query(Borrow).filter(
        Borrow.book_id == book_id,
        Borrow.stud_id == student_id,
        Borrow.return_date == None
    ).first()

    if borrow is None:
        db.close()
        return "Borrow record not found"

    book = db.query(Book).filter(
        Book.id == book_id
    ).first()

    if book is None:
        db.close()
        return "Book not found"

    # Current date/time
    return_date = datetime.now()

    # Calculate number of days borrowed
    days_borrowed = (return_date - borrow.borrow_date).days

    # Allowed borrowing period
    allowed_days = 14

    # Fine per late day
    fine_per_day = 10

    # Calculate fine
    if days_borrowed > allowed_days:
        late_days = days_borrowed - allowed_days
        fine = late_days * fine_per_day
    else:
        late_days = 0
        fine = 0

    # Save return date and fine
    borrow.return_date = return_date
    borrow.fine = fine

    db.commit()

    # If there is a fine, go to payment page
    if fine > 0:
        db.close()

        return RedirectResponse(
            url=f"/payment/{borrow.id}",
            status_code=303
        )

    # No fine → make book available
    book.available = True

    db.commit()
    db.close()

    return "Book returned successfully"

@app.get("/add-book",response_class=HTMLResponse)  
def add(request:Request):
    return templates.TemplateResponse("add.html",{
                                     "request":request
                                    })  

@app.post("/add-book")
def add(title: str = Form(...),
        author: str = Form(...),
        category: str = Form(...)):
    db=SessionLocal()
    book=Book()
    book.title=title
    book.author=author
    book.category=category
    book.available=True
    db.add(book)
    db.commit()

    db.close()
    return RedirectResponse(url="/add-book", status_code=303)

@app.get("/books",response_class=HTMLResponse)
def show(request:Request):
    db=SessionLocal()
    books=db.query(Book).all()
    db.close()
    return templates.TemplateResponse("books.html",{
        "request":request,
        "books":books
    })

@app.get("/mybooks", response_class=HTMLResponse)
def my_books(request: Request):

    student_id = request.session.get("student_id")

    if student_id is None:
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()

    borrowed = db.query(Borrow).filter(
        Borrow.stud_id == student_id,
        Borrow.return_date == None
    ).all()

    books = []

    for borrow in borrowed:

        book = db.query(Book).filter(
            Book.id == borrow.book_id
        ).first()

        if book:
            books.append({
                "borrow": borrow,
                "book": book
            })

    db.close()

    return templates.TemplateResponse(
        "my_books.html",
        {
            "request": request,
            "books": books
        }
    )

@app.get("/logout")
def logout(request:Request):
    request.session.clear()
    return RedirectResponse(url="/login",status_code=303)