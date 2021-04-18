from sqlalchemy.orm import Session

import models, schemas


def get_all(db: Session):
    return db.query(models.InfectedData).all()


def get_most_recent_infected_data(db: Session):
    most_recent_query = db.query(models.InfectedData).first()
    return db.query(models.InfectedData).filter(models.InfectedData.date == most_recent_query.date).all()


def get_data_by_number(db: Session, number: int):
    return db.query(models.InfectedData).filter(models.InfectedData.number == number).first()


def create_infected_data(db: Session, data: schemas.InfectedDataCreate):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data
