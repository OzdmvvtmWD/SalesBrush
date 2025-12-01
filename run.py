import datetime
import json
from loguru import logger
import pandas as pd
from handler_DB.settings.settings import SessionLocal
from handler_DB.models.models import DailyStats 

def create_in_db(data:dict):
    try:
        db = SessionLocal()
        daily_stats = DailyStats(
            date = data.get('date'),
            campaign_id = data.get('campaign_id'),
            spend = data.get('spend'),
            conversions = data.get('conversions'),
            CPA = data.get('CPA'),
        )
        db.merge(daily_stats)
        db.commit()
    except Exception as e:
        print(e)

def upsert(users: dict, update=True):
    entries_to_update = 0
    entries_to_put = []

    db = SessionLocal()

    for each in (
        db.query(DailyStats.id)
        .filter(DailyStats.id.in_(users.keys()))
        .all()
    ):
        values = users.pop(each.id)
        entries_to_update += 1
        if update:
            db.merge(DailyStats(**values))

    for u in users.values():
        entries_to_put.append(u)

    db.bulk_insert_mappings(DailyStats, entries_to_put)
    db.commit()

    return (
        f" inserted:\t{len(entries_to_put)}\n"
        f" {'updated' if update else 'not updated'}:\t{str(entries_to_update)}"
    )

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
    except Exception as e:
        return None
    
def get_func_2(start_date: str, end_date: str, old_json: list, incoming_json: list):
   
    try:
       
        filtered_spend = get_func_1(start_date, end_date, old_json)
        filtered_conversions = get_func_1(start_date, end_date, incoming_json)

        df_spend = pd.DataFrame(filtered_spend)
        df_conversions = pd.DataFrame(filtered_conversions)
        
        df_merged = pd.merge(
            df_spend, 
            df_conversions, 
            on=['date', 'campaign_id'], 
            how='outer'
        )

       
        df_merged['CPA'] = df_merged.apply(
            lambda row: save_division(row['spend'], row['conversions'], round_result=2), 
            axis=1
        )
        
        df_merged = df_merged[['date', 'campaign_id', 'spend', 'conversions', 'CPA']]

        final_data = []
        for record in df_merged.to_dict('records'):
            new_record = {}
            for k, v in record.items():
                new_record[k] = nan_to_none(v)
            final_data.append(new_record)
        
        return final_data
        
    except Exception as e:
        logger.error(f"Error in get_func_2: {e}")
        return []

def nan_to_none(value):
    if pd.isna(value):
        return None
    if isinstance(value, float) and value == int(value) and value >= 0:
        return int(value)
    return value

json_file_1 = read_json_file(r'C:\Users\Admin\projects\SalesBrush\json_files\fb_spend.json')
json_file_2 = read_json_file(r'C:\Users\Admin\projects\SalesBrush\json_files\network_conv.json')


res_3 = get_func_2('2025-06-01', '2025-06-11', json_file_1, json_file_2)
print(json.dumps(res_3, indent=4))


columns = ['date', 'campaign_id', 'spend', 'conversions', 'CPA']

d = pd.DataFrame(data=res_3, columns=columns)
users = {
    f"{row['date']}_{row['campaign_id']}": row
    for row in res_3
}

result = upsert(users)
print(result)
