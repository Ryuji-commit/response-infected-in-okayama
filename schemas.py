from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class InfectedDataBase(BaseModel):
    number: int
    date: datetime
    age: int
    sex: str
    residence: str


class InfectedDataCreate(InfectedDataBase):
    number: int
    date: datetime
    age: int
    sex: str
    residence: str


class InfectedData(InfectedDataBase):
    number: int
    date: datetime
    age: int
    sex: str
    residence: str

    class Config:
        orm_mode = True
