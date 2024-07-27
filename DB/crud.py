from sqlalchemy.orm import Session
from DB import modals, schemas

def create_author(db: Session, name: str, second_name: str, info: str):
    db_author = modals.DBAuthor(name=name, second_name=second_name, info=info)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_author(db: Session, author_id: int):
    return db.query(modals.DBAuthor).filter(modals.DBAuthor.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 66):
    return db.query(modals.DBAuthor).offset(skip).limit(limit).all()

def create_book(db: Session, title, pages, author_id, info: str):
    db_book = modals.DBBook(title=title, pages=pages, author_id=author_id, info=info)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(modals.DBBook).filter(modals.DBBook.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 50):
    return db.query(modals.DBBook).offset(skip).limit(limit).all()