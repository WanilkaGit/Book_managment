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
def start(request:Request, skip: int=0 , limit: int=50, db:Session= Depends(get_db)):
    return template.TemplateResponse("main.html", {'request': request})

@app.get("/login")
def login(request: Request):
    return template.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != username or form_data.password != password:
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")
    {"access_token": form_data.username, "token_type": "bearer"}
    login_complete = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Page</title>
    </head>
    <body>
        <h1>Login complete</h1>
    </body>
    </html>
    """
    HTMLResponse(content=login_complete)

    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Ці дані доступні лише авторизованим користувачам"}


@app.get('/author/add/ask/', response_model=schemas.Author)
def add_author(request:Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("add_author.html", {'request': request})


@app.post('/author/add/result/', response_model=schemas.Author)
def add_author(db: Session = Depends(get_db), name: str = Form(...), second_name: str = Form(...)):
    crud.create_author(db=db, name=name, second_name=second_name)
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Page</title>
    </head>
    <body>
        <h1>Author have added complete</h1>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get('author/get/', response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)


@app.get("/authorlist/")
def authorlist(request:Request, skip: int=0 , limit: int=50, db:Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return template.TemplateResponse("authorlist.html", {'request': request, 'authors': authors})

@app.get('/author/add/ask/', response_model=schemas.Author)
def add_author(request:Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("add_author.html", {'request': request})

@app.get('/book/add/ask/', response_model=schemas.Author)
def add_author(request:Request, db: Session = Depends(get_db)):
    return template.TemplateResponse("add_book.html", {'request': request})

@app.post('/book/add/result', response_model=schemas.Book)
def add_book(db: Session = Depends(get_db), curent_user: str = Depends(protected), title: str = Form(...), pages: int = Form(...), author_id: int = Form(...)):
    crud.create_book(db=db, author_id=author_id, title=title, pages=pages)
    return print("0")


@app.get('/book/get/', response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db), curent_user: str = Depends(protected)):
    return crud.get_book(db, book_id)


@app.get("/booklist/")
def booklist(request:Request, skip: int=0 , limit: int=50, db:Session= Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return template.TemplateResponse("booklist.html", {'request': request, 'books': books})