from sqlalchemy.orm import Session

from . import models, schemas


def get_all(db: Session):
    return db.query(models.InfectedData).all()


def get_most_recent_infected_data(db: Session):
    most_recent_query = db.query(models.InfectedData).first()
    return db.query(models.InfectedData).filter(models.InfectedData.date == most_recent_query.date).all()


def create_infected_data(db: Session, data: schemas.InfectedDataCreate, crawled_data: dict):
    db_infected_data = models.InfectedData(number=crawled_data["number"],
                                           date=crawled_data["date"],
                                           age=crawled_data["age"],
                                           sex=crawled_data["sex"],
                                           residence=crawled_data["residence"]
                                           )
    db.add(db_infected_data)
    db.commit()
    db.refresh(db_infected_data)
    return db_infected_data
