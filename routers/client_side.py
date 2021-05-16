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


@router.get("/countBy/{column_name}", tags=["client"])
async def get_count(
        column_name: models.ColumnName,
        start_date_str: Optional[str] = None,
        end_date_str: Optional[str] = None,
        db: Session = Depends(get_db)):
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
    counts = crud.get_count(db=db, column_name=column_name, start_date=start_date, end_date=end_date)
    return counts


@router.get("/allMistakenData/", response_model=List[schemas.MistakenData], tags=["client"])
async def get_all_mistaken_data(db: Session = Depends(get_db)):
    items = crud.get_all_mistaken_data(db=db)
    return items
