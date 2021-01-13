from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import  BaseModel
from pyquery import PyQuery
import requests
import re
import datetime


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.0


app = FastAPI()


@app.get("/data/")
async def read_item():
    result = crawl_infected_person_okayama()
    return result


def crawl_infected_person_okayama():
    try:
        response = requests.get('https://www.pref.okayama.jp/page/667843.html')
        response.encoding = response.apparent_encoding
        doc = PyQuery(response.text.encode('utf-8'))
    except Exception as e:
        return {"exception": e.args}

    result = []
    for tr_node in doc.find('tbody').children('tr'):
        td_nodes = PyQuery(tr_node)('tr').find('td')
        valid_values = validate_crawled_data(
            td_nodes.eq(0).text(),
            td_nodes.eq(1).text(),
            td_nodes.eq(2).text(),
            td_nodes.eq(3).text(),
            td_nodes.eq(4).text()
        )
        if not valid_values:
            continue
        result.append(valid_values)

    return result


def validate_crawled_data(number: str, date: str, age: str, sex: str, residence: str):
    valid_number = validate_number(number)
    if valid_number is False:
        return False

    calculated_year = calculate_year(valid_number)
    valid_date = validate_date(date, calculated_year)
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

    return {
            "number": valid_number,
            "date": valid_date,
            "age": valid_age,
            "sex": valid_sex,
            "residence": valid_residence,
    }


def validate_number(number: str):
    is_integer = re.compile(r'^\d+$', flags=re.MULTILINE)
    if is_integer.match(number) is None:
        print(number, flush=True)
        return False
    return int(number)


# need to fix!!
def calculate_year(valid_number: int):
    if valid_number >= 1364:
        return 2021
    else:
        return 2020


# (月|日)は元のサイトの誤字
def validate_date(date: str, year: int):
    is_date = re.compile(r'^(?P<month>\d+)(月|日)(?P<day>\d+)日$', flags=re.MULTILINE)
    match_date = is_date.match(date)
    if match_date is None:
        print(date, flush=True)
        return False

    month = int(match_date.group('month'))
    day = int(match_date.group('day'))
    return datetime.date(year, month, day)


def determine_is_disclosed(string: str):
    is_disclosed = re.compile(r'非公表', flags=re.MULTILINE)
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



