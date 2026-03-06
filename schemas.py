from pydantic import BaseModel
from typing import Optional


class Userschemas(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    id_card: str
    amount: int

    class Config:
        orm_mode = True

    class Config:
        from_attribute = True


class Bookschemas(BaseModel):
    name: str
    writer: str
    category: str
    isbn: str

    class Config:
        from_attribute = True

