from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

from sqlalchemy.orm import Session
from DB.engine import SessionLocal, engine

from typing_extensions import Annotated

from DB import modals, schemas, crud

#fastapi dev main.py

modals.Base.metadata.create_all(bind=engine)

app = FastAPI()

template = Jinja2Templates(directory="templates")
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
app.mount("/CSS", StaticFiles(directory="css"), name="css")
# app.mount("/img", StaticFiles(directory="img"), name="img")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

username = 'admin'
password = '1'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
def start(request:Request, skip: int=0 , limit: int=50):
    return template.TemplateResponse("main.html", {'request': request})


@app.get("/login")
def login(request: Request):
    return template.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != username or form_data.password != password:
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")
    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Ці дані доступні лише авторизованим користувачам"}


@app.get('/author/add/ask/', response_model=schemas.Author)
def add_author(request:Request):
    return template.TemplateResponse("add_author.html", {'request': request})

@app.post('/author/add/result/', response_model=schemas.Author)
def add_author(db: Session = Depends(get_db), name: str = Form(...), second_name: str = Form(...), info: str =Form(...)):
    crud.create_author(db=db, name=name, second_name=second_name, info=info)
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="/CSS/style.css" rel="stylesheet">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Booklist</title>
    </head>
    <body>
        <h1>Author have added complete</h1>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get('/author/get/ask/', response_model=schemas.Author)
def get_author(request:Request):
    return template.TemplateResponse("get_author.html", {'request': request})

@app.post('/author/get/result/', response_model=schemas.Author)
def get_author(request: Request, author_id: int = Form(...), db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id)
    return template.TemplateResponse("get_author_res.html", {'request': request, "author": author})


@app.get("/author/list/")
def authorlist(request:Request, skip: int=0 , limit: int=50, db:Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return template.TemplateResponse("authorlist.html", {'request': request, 'authors': authors})



@app.get('/book/add/ask/', response_model=schemas.Author)
def add_author(request:Request):
    return template.TemplateResponse("add_book.html", {'request': request})

@app.post('/book/add/result', response_model=schemas.Book)
def add_book(db: Session = Depends(get_db), title: str = Form(...), pages: int = Form(...), author_id: int = Form(...), info: str =Form(...), current_user: str = Depends(protected)):#, curent_user: str = Depends(protected)
    crud.create_book(db=db, author_id=author_id, title=title, pages=pages, info=info)
    html_add_book_result = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="/CSS/style.css" rel="stylesheet">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Booklist</title>
    </head>
    <body>
        <h1>Book aded to site library</h1>
    </body>
    </html>
    """
    return HTMLResponse(content=html_add_book_result)

@app.post('/book/get/ask', response_model=schemas.Book)
def get_book(request:Request):
    return template.TemplateResponse("get_book.html", {'request': request})

@app.post('/book/get/result', response_model=schemas.Book)
def get_book(request:Request, book_id: int  = Form(...), db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    return template.TemplateResponse("get_book_res.html", {'request': request, 'book': book})


@app.get("/book/list/")
def booklist(request:Request, skip: int=0 , limit: int=50, db:Session= Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return template.TemplateResponse("booklist.html", {'request': request, 'books': books})