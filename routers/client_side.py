from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
import datetime

import crud
import models
import schemas
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/mostRecentData/", response_model=List[schemas.InfectedData], tags=["client"])
async def get_recent_data(db: Session = Depends(get_db)):
    items = crud.get_most_recent_infected_data(db=db)
    return items


@router.get("/allDataNum/", tags=["client"])
async def get_all_data_num(db: Session = Depends(get_db)):
    num = crud.get_all_data_num(db=db)
    return num


@router.get("/recentDataNum/", tags=["client"])
async def get_recent_data_num(db: Session = Depends(get_db)):
    recent_date = crud.get_recent_date(db=db)
    num = crud.get_recent_data_num(db=db)
    return {
        "date": recent_date,
        "number": num,
    }


@router.get("/recentDate/", tags=["client"])
async def get_recent_date(db: Session = Depends(get_db)):
    recent_date = crud.get_recent_date(db=db)
    return recent_date


@router.get("/countByResidence/{start_date_str}/{end_date_str}", tags=["client"])
async def get_all_data_num(start_date_str: str, end_date_str: str, db: Session = Depends(get_db)):
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    num = crud.get_count_by_residence(db=db, start_date=start_date, end_date=end_date)
    return num


@router.get("/allMistakenData/", response_model=List[schemas.MistakenData], tags=["client"])
async def get_all_mistaken_data(db: Session = Depends(get_db)):
    items = crud.get_all_mistaken_data(db=db)
    return items
