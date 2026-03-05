from pydantic import BaseModel
from typing import Optional


class Userschemas(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    id_card: int

    class Config:
        from_attribute = True

