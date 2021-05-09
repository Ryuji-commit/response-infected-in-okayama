from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

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
