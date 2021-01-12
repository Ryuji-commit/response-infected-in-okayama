from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import  BaseModel
from pyquery import PyQuery
import requests
import re


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

    target_table_body = doc.find('tbody')[0]
    result = []
    for tr_node in doc.find('tbody').children('tr'):
        td_nodes = PyQuery(tr_node)('tr').find('td')

        validate_val = validate_crawled_data(
            td_nodes.eq(0).text(),
            td_nodes.eq(1).text(),
            td_nodes.eq(2).text(),
            td_nodes.eq(3).text(),
            td_nodes.eq(4).text()
        )

        if not validate_val:
            continue

        result.append({
            "number": validate_val[0],
            "date": validate_val[1],
            "age": validate_val[2],
            "sex": validate_val[3],
            "residence": validate_val[4],
        })
    print(result, flush=True)
    return result


def validate_crawled_data(number, date, age, sex, residence):
    is_integer = re.compile(r'^\d+$', flags=re.MULTILINE)
    is_date = re.compile(r'^(\d+)月(\d+)日$', flags=re.MULTILINE)
    is_age = re.compile(r'^((\d+)代|\((.*?)市非公表\))$', flags=re.MULTILINE)
    is_sex = re.compile(r'^((.性)|\((.*?)市非公表\))$', flags=re.MULTILINE)
    is_residence = re.compile(r'(^.*?(町|市|都|府|道|県)$|^\((.*?)市非公表\)$)', flags=re.MULTILINE)

    if is_integer.match(number) is None:
        return False
    if is_date.match(date) is None:
        return False
    if is_age.match(age) is None:
        return False
    if is_sex.match(sex) is None:
        return False
    if is_residence.match(residence) is None:
        return False

    return [number, date, age, sex, residence]



