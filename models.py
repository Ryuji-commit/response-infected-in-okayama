from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from database import Base


class InfectedData(Base):
    __tablename__ = "infected_data"

    number = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=True)
    age = Column(Integer, index=True, nullable=True)
    sex = Column(String(10), index=True, nullable=True)
    residence = Column(String(50), index=True, nullable=True)


class MistakenData(Base):
    __tablename__ = "mistaken_data"

    number_str = Column(String(50), primary_key=True, index=True)
    date_str = Column(String(50), nullable=True, index=True)
    age_str = Column(String(50), nullable=True, index=True)
    sex_str = Column(String(50), nullable=True, index=True)
    residence_str = Column(String(50), nullable=True, index=True)
