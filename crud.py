from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy import func
import datetime

import models, schemas


def get_all_data_num(db: Session):
    return db.query(models.InfectedData).count()


def get_recent_data_num(db: Session):
    most_recent_query = db.query(models.InfectedData).order_by(desc(models.InfectedData.number)).first()
    return db.query(models.InfectedData).filter(models.InfectedData.date == most_recent_query.date).count()


def get_most_recent_infected_data(db: Session):
    most_recent_query = db.query(models.InfectedData).order_by(desc(models.InfectedData.number)).first()
    most_recent_data = db.query(models.InfectedData).filter(models.InfectedData.date == most_recent_query.date)\
        .order_by(desc(models.InfectedData.number)).all()
    if most_recent_data is None:
        return []
    return most_recent_data


def get_recent_date(db: Session):
    most_recent_query = db.query(models.InfectedData).order_by(desc(models.InfectedData.number)).first()
    return most_recent_query.date


def get_data_by_number(db: Session, number: int):
    return db.query(models.InfectedData).filter(models.InfectedData.number == number).first()


# 開始日以降終了日以前(その日だけ欲しい場合はstartとend共にその日付を指定)
def get_count(db: Session, column_name: models.ColumnName, start_date: datetime.date, end_date: datetime.date):
    select_column = column_name.col
    result = db.query(select_column, func.count(models.InfectedData.number).label('count'))
    if not(start_date is None or end_date is None):
        result = result.filter(
            models.InfectedData.date >= start_date, models.InfectedData.date <= end_date
        )
    result = result.group_by(select_column).all()
    return result


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


def delete_all_mistaken_data(db: Session):
    exist = db.query(models.MistakenData).first is not None
    if exist:
        db.query(models.MistakenData).delete()
