import os
import sys
import json
import datetime
import pandas as pd
from loguru import logger

from CONFIG import LOGS_DIR


logger.add(sys.stderr, format="{time} {level} {message}",  level="INFO")
logger.add(os.path.join(LOGS_DIR, "utils_{time}.log"))

def read_json_file(path: str):
    logger.debug(f"Reading JSON file: {path}")
    try:
        with open(path, 'r') as f:
            data = json.loads(f.read())
            logger.info(f"Loaded JSON file successfully: {path}, records={len(data)}")
            return data
    except Exception as error:
        logger.exception(f"Failed to read JSON file: {path} — {error}")
        return {}


def ISO_format(date: str):
    strptime_format = '%Y-%m-%d'

    try:
        result = datetime.datetime.strptime(date, strptime_format)
        return result
    except ValueError:
        logger.error(f"Invalid date format: {date}")
        return None
    except Exception as e:
        logger.exception(f"Unexpected error in ISO_format({date}): {e}")
        return None


def save_division(a: float, b: float, round_result: int = 1):
    try:
        result = round(a / b, round_result)
        return result
    except Exception:
        logger.warning(f"Division error: a={a}, b={b}")
        return None


def get_days_intervals(start_date: str, end_date: str, json_obj: list):
    logger.debug(f"Filtering records between {start_date} and {end_date}")

    try:
        filtered = [
            element for element in json_obj
            if ISO_format(element['date']) >= ISO_format(start_date)
            and ISO_format(element['date']) <= ISO_format(end_date)
        ]

        logger.info(f"Filtered {len(filtered)} records in date range {start_date} → {end_date}")
        return filtered

    except Exception as e:
        logger.exception(f"Error in get_days_intervals(): {e}")
        return []


def nan_to_none(value):
    if pd.isna(value):
        logger.debug("Converted NaN → None")
        return None

    if isinstance(value, float) and value == int(value) and value >= 0:
        return int(value)

    return value
