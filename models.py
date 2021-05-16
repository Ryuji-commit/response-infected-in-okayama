from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from enum import Enum, auto

from database import Base


class InfectedData(Base):
    __tablename__ = "infected_data"

    number = Column(Integer, primary_key=True)
    date = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)
    residence = Column(String(50), nullable=True)


class MistakenData(Base):
    __tablename__ = "mistaken_data"

    number_str = Column(String(50), primary_key=True)
    date_str = Column(String(50), nullable=True)
    age_str = Column(String(50), nullable=True)
    sex_str = Column(String(50), nullable=True)
    residence_str = Column(String(50), nullable=True)


# Enumを指定(データベースとは無関係)
class ColumnName(Enum):
    date = ("date", InfectedData.date)
    age = ("age", InfectedData.age)
    sex = ("sex", InfectedData.sex)
    residence = ("residence", InfectedData.residence)

    def __new__(cls, value, col):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.col = col
        return obj
