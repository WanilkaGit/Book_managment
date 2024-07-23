from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != username or form_data.password != password:
        raise HTTPException(status_code = 400, detail = "Incorrect username or password")

    return {"access_token": form_data.username, "token_type": "bearer"}

@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    return {"message": "Ці дані доступні лише авторизованим користувачам"}

@app.post('/author/add/', response_model=schemas.Author)
def add_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get('author/get/', response_model=schemas.Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author(db, author_id)

@app.post('/{author_id}/add/', response_model=schemas.Book)
def add_book(book: schemas.BookCreate, author_id: int, db: Session = Depends(get_db), curent_user: str = Depends(protected)):
    return crud.create_book(db=db, book=book, author_id=author_id)

@app.get('/book/get/', response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db), curent_user: str = Depends(protected)):
    return crud.get_book(db, book_id)

@app.get("/booklist/")
def booklist(request:Request, skip: int=0 , limit: int=50, db:Session= Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return template.TemplateResponse("books_info.html", {'request': request, 'books': books})