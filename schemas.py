from typing import List, Optional
import datetime
from pydantic import BaseModel


class InfectedDataBase(BaseModel):
    number: int
    date: datetime.date = None
    age: int = None
    sex: str = None
    residence: str = None


class InfectedDataCreate(InfectedDataBase):
    number: int
    date: datetime.date = None
    age: int = None
    sex: str = None
    residence: str = None


class InfectedData(InfectedDataBase):
    number: int
    date: datetime.date = None
    age: int = None
    sex: str = None
    residence: str = None

    class Config:
        orm_mode = True
