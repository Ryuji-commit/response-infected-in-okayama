from pyquery import PyQuery
import requests
import re
import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, APIRouter

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/saveCrawledUnsavedValue/", tags=["background"])
def save_crawled_data(db: Session = Depends(get_db)):
    try:
        response_message = crawl_infected_person_okayama(db=db, is_update=False)
        return response_message
    except IntegrityError as e:
        return e


@router.get("/updateSavedValue/", tags=["background"])
def update_saved_data(db: Session = Depends(get_db)):
    try:
        response_message = crawl_infected_person_okayama(db=db, is_update=True)
        return response_message
    except IntegrityError as e:
        return e


def crawl_infected_person_okayama(db: Session = Depends(get_db), is_update: bool = False):
    try:
        response = requests.get('https://fight-okayama.jp/attribute/')
        response.encoding = response.apparent_encoding
        doc = PyQuery(response.text.encode('utf-8'))
    except Exception as e:
        return {"exception": e.args}

    updated_num = 0
    saved_num = 0

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
            if crud.get_mistaken_data_by_number(db=db, number_str=td_nodes.eq(0).text()) is None:
                create_mistaken_data(models.MistakenData(
                    number_str=td_nodes.eq(0).text(),
                    date_str=td_nodes.eq(1).text(),
                    residence_str=td_nodes.eq(2).text(),
                    age_str=td_nodes.eq(3).text(),
                    sex_str=td_nodes.eq(4).text()
                ), db=db)
            continue

        # 値が既に存在していた場合、is_updateがTrueであればUPDATE
        if crud.get_data_by_number(db=db, number=valid_values.number) is not None:
            if is_update:
                update_infected_data(data=valid_values, db=db)
                updated_num += 1
            else:
                return "the crawled data is existing"
        # 値が存在していない場合、値を保存
        else:
            create_infected_data(data=valid_values, db=db)
            saved_num += 1

    return {
        "updated": "{}items".format(updated_num),
        "saved": "{} items".format(saved_num),
    }


@router.get("/saveMistakenFormatData/", tags=["background"])
def save_mistaken_format_data(db: Session = Depends(get_db)):
    mistaken_format_data = [(validate_crawled_data(number="1320",
                                                   date="2020/12/30",
                                                   age="50代",
                                                   sex="女性",
                                                   residence="倉敷市"))]
    saved_num = 0
    for data in mistaken_format_data:
        if crud.get_data_by_number(db=db, number=data.number) is not None:
            continue
        else:
            create_infected_data(data=data, db=db)
            saved_num += 1
    return {"saved": "{} mistaken items".format(saved_num)}


def create_infected_data(data: schemas.InfectedDataCreate, db: Session = Depends(get_db)):
    return crud.create_infected_data(db=db, data=data)


def update_infected_data(data: schemas.InfectedDataCreate, db: Session = Depends(get_db)):
    return crud.update_infected_data(db=db, data=data)


def create_mistaken_data(data: schemas.MistakenDataCreate, db: Session = Depends(get_db)):
    return crud.create_mistaken_data(db=db, data=data)


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
