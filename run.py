import datetime
import json
from loguru import logger

def read_json_file(path:str):
    try:
        with open(path, 'r') as f:
            return json.loads(f.read())
    except Exception as error:
        return {}
  

def ISO_format(date: str):
    strptime_format = '%Y-%m-%d'

    try:
        return datetime.datetime.strptime(date, strptime_format)
    except ValueError:
        print('date fail')
        return None


def get_func_1(start_date: str, end_date:str, json_obj: list):
    try:
        return [element for element in json_obj \
            if ISO_format(element['date']) >= ISO_format(start_date) and ISO_format(element['date']) <= ISO_format(end_date)]
    except Exception as e:
        print(e)
  
def save_division(a: float, b: float, round_result:int= 1):
    try:
        return round(a/b, round_result)
    except ZeroDivisionError as e:
        return None

def get_func_2(start_date: str, end_date: str, old_json, incoming_json):
    old = get_func_1(start_date, end_date, old_json)
    incoming = get_func_1(start_date, end_date, incoming_json)

    combined = {}

    for item in old:
        date = item["date"]
        combined[date] = item.copy()

    for item in incoming:
        date = item["date"]

        if date not in combined:
            combined[date] = item.copy()
        else:
            for key, value in item.items():
                if key == "date":
                    continue

                if isinstance(value, list) and isinstance(combined[date].get(key), list):
                    combined[date][key].extend(value)
                else:
                    combined[date][key] = value

        spend = combined[date].get("spend")
        conversions = combined[date].get("conversions")

        combined[date]["CPA"] = save_division(spend, conversions)

    return list(combined.values())


json_file_1 = read_json_file(r'C:\Users\Admin\projects\SalesBrush\fb_spend.json')
json_file_2 = read_json_file(r'C:\Users\Admin\projects\SalesBrush\network_conv.json')


res_3 = get_func_2('2025-06-05', '2025-06-11', json_file_1, json_file_2)
print(res_3)
