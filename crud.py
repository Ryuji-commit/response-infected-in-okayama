from sqlalchemy.orm import Session

import models, schemas


def get_all(db: Session):
    all_data = db.query(models.InfectedData).all()
    if all_data is None:
        return []
    return all_data


def get_all_data_num(db: Session):
    return db.query(models.InfectedData).count()


def get_recent_data_num(db: Session):
    most_recent_query = db.query(models.InfectedData).first()
    return db.query(models.InfectedData).filter(models.InfectedData.date == most_recent_query.date).count()


def get_most_recent_infected_data(db: Session):
    most_recent_query = db.query(models.InfectedData).first()
    most_recent_data = db.query(models.InfectedData).filter(models.InfectedData.date == most_recent_query.date).all()
    if most_recent_data is None:
        return []
    return most_recent_data


def get_data_by_number(db: Session, number: int):
    return db.query(models.InfectedData).filter(models.InfectedData.number == number).first()


def create_infected_data(db: Session, data: schemas.InfectedDataCreate):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def update_infected_data(db: Session, data: schemas.InfectedDataCreate):
    update_query = db.query(models.InfectedData).filter(models.InfectedData.number == data.number).first()
    update_query.date = data.date
    update_query.age = data.age
    update_query.sex = data.sex
    update_query.residence = update_query.residence


def create_mistaken_data(db: Session, data: schemas.MistakenDataCreate):
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def get_all_mistaken_data(db: Session):
    all_data = db.query(models.MistakenData).all()
    if all_data is None:
        return []
    return all_data


def get_mistaken_data_by_number(db: Session, number_str: str):
    return db.query(models.MistakenData).filter(models.MistakenData.number_str == number_str).first()
