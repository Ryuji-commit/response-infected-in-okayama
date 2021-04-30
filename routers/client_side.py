from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session

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


@router.get("/allData/", response_model=List[schemas.InfectedData], tags=["client"])
async def get_all_data(db: Session = Depends(get_db)):
    items = crud.get_all(db=db)
    return items


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
    num = crud.get_recent_data_num(db=db)
    return num


@router.get("/recentDate/", tags=["client"])
async def get_recent_date(db: Session = Depends(get_db)):
    recent_date = crud.get_recent_date(db=db)
    return recent_date


@router.get("/allMistakenData/", response_model=List[schemas.MistakenData], tags=["client"])
async def get_all_mistaken_data(db: Session = Depends(get_db)):
    items = crud.get_all_mistaken_data(db=db)
    return items
