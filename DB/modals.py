from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .engine import Base

class DBAuthor(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False)
    second_name = Column(String(64), nullable=False)


class DBBook(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(64), nullable=False)
    # book_info = Column(String(264), nullable=False)
    pages = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey("author.id"))

    author = relationship(DBAuthor)


class DBUser(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)