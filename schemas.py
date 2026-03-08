from pydantic import BaseModel


class Userschemas(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    id_card: str

    class Config:
        from_attribute = True


class Bookschemas(BaseModel):
    name: str
    writer: str
    category: str
    isbn: str


    class Config:
        from_attribute = True


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attribute = True


class LoanSchema(BaseModel):
    book_id: int
    days: int

    class Config:
        from_attribute = True
