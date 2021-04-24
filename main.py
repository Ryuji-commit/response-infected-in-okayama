from typing import Optional, List
from pydantic import BaseModel
from pyquery import PyQuery
import requests
import re
import datetime
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/data/", response_model=List[schemas.InfectedData])
async def read_item(db: Session = Depends(get_db)):
    crawl_infected_person_okayama(db=db)
    items = crud.get_all(db=db)
    return items


def crawl_infected_person_okayama(db: Session = Depends(get_db)):
    try:
        response = requests.get('https://fight-okayama.jp/attribute/')
        response.encoding = response.apparent_encoding
        doc = PyQuery(response.text.encode('utf-8'))
    except Exception as e:
        return {"exception": e.args}

    for tr_node in doc.find('tbody').children('tr'):
        td_nodes = PyQuery(tr_node)('tr').find('td')
        valid_values = validate_crawled_data(
            number=td_nodes.eq(0).text(),
            date=td_nodes.eq(1).text(),
            residence=td_nodes.eq(2).text(),
            age=td_nodes.eq(3).text(),
            sex=td_nodes.eq(4).text()
        )
        if not valid_values:
            continue

        # もしクロールしたnumberが存在していれば保存せずクロールを終了(クロール自体は行うため変更の必要あり)
        if crud.get_data_by_number(db=db, number=valid_values.number) is not None:
            return
        create_infected_data(data=valid_values, db=db)


def create_infected_data(data: schemas.InfectedDataCreate, db: Session = Depends(get_db)):
    return crud.create_infected_data(db=db, data=data)


def validate_crawled_data(number: str, date: str, age: str, sex: str, residence: str):
    valid_number = validate_number(number)
    if valid_number is False:
        return False

    valid_date = validate_date(date)
    if valid_date is False:
        return False

    valid_age = validate_age(age)
    if valid_age is False:
        return False

    valid_sex = validate_sex(sex)
    if valid_sex is False:
        return False

    valid_residence = validate_residence(residence)
    if valid_residence is False:
        return False

    return models.InfectedData(
        number=valid_number,
        date=valid_date,
        age=valid_age,
        sex=valid_sex,
        residence=valid_residence
    )


def validate_number(number: str):
    is_integer = re.compile(r'^\d+$', flags=re.MULTILINE)
    if is_integer.match(number) is None:
        print(number, flush=True)
        return False
    return int(number)


def validate_date(date: str):
    is_date = re.compile(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', flags=re.MULTILINE)
    match_date = is_date.match(date)
    if match_date is None:
        print(date, flush=True)
        return False

    year = int(match_date.group('year'))
    month = int(match_date.group('month'))
    day = int(match_date.group('day'))
    return datetime.date(year, month, day)


def determine_is_disclosed(string: str):
    is_disclosed = re.compile(r'^(ー|非公表)$', flags=re.MULTILINE)
    if is_disclosed.search(string) is not None:
        return True
    return False


def validate_age(age: str):
    is_age = re.compile(r'^(?P<age>\d+)(歳|代)(以上|未満)?$', flags=re.MULTILINE)
    is_preschooler = re.compile(r'^未就学児$', flags=re.MULTILINE)
    match_age = is_age.match(age)
    if match_age is not None:
        return int(match_age.group('age'))
    elif is_preschooler.match(age) is not None:
        return 0
    else:
        if determine_is_disclosed(age):
            return None
        else:
            print(age, flush=True)
            return False


def validate_sex(sex: str):
    is_sex = re.compile(r'^(男|女)性$', flags=re.MULTILINE)
    if is_sex.match(sex) is not None:
        return sex
    else:
        if determine_is_disclosed(sex):
            return None
        else:
            print(sex, flush=True)
            return False


def validate_residence(residence: str):
    is_residence = re.compile(
        r'^(?P<residence>((.+?(町|市|都|府|道|県|村))$|(県|国)外$|県内)).*?',
        flags=re.MULTILINE)
    match_residence = is_residence.match(residence)
    if match_residence is not None:
        return match_residence.group('residence')
    else:
        if determine_is_disclosed(residence):
            return None
        else:
            print(residence, flush=True)
            return False



