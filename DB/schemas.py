from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    second_name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    pages: int
    author_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    login: str
    password: str

class UserCreate(UserBase): pass 

class User(UserBase):
    id: int

    class Config:
        from_attributes = True