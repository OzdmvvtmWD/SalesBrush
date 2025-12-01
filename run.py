import os
import json
import sys
from loguru import logger
import pandas as pd

from handler_DB.operations import upsert, query_by_date
from utils.utils import *
from CONFIG import JSON_DIR, LOGS_DIR

logger.add(sys.stderr, format="{time} {level} {message}",  level="INFO")
logger.add(os.path.join(LOGS_DIR, "run_{time}.log"))

def run_func(start_date: str, end_date: str, json_path_1: str, json_path_2: str):
    logger.info(f"run_func started with date range {start_date} → {end_date}")
    logger.debug(f"JSON Path 1: {json_path_1}")
    logger.debug(f"JSON Path 2: {json_path_2}")

    try:
        old_json = read_json_file(json_path_1)
        incoming_json = read_json_file(json_path_2)
        logger.info(f"Loaded JSON files: old_json={len(old_json)}, incoming_json={len(incoming_json)}")

        filtered_spend = get_days_intervals(start_date, end_date, old_json)
        filtered_conversions = get_days_intervals(start_date, end_date, incoming_json)
        logger.info(f"Filtered records: spend={len(filtered_spend)}, conversions={len(filtered_conversions)}")

        df_spend = pd.DataFrame(filtered_spend)
        df_conversions = pd.DataFrame(filtered_conversions)
        logger.debug("DataFrames created")

        df_merged = pd.merge(
            df_spend,
            df_conversions,
            on=['date', 'campaign_id'],
            how='outer'
        )
        logger.info(f"Merged dataframe size: {len(df_merged)}")

        df_merged['CPA'] = df_merged.apply(
            lambda row: save_division(row['spend'], row['conversions'], round_result=2),
            axis=1
        )
        logger.debug("CPA calculation completed")

        df_merged = df_merged[['date', 'campaign_id', 'spend', 'conversions', 'CPA']]

        final_data = []
        for record in df_merged.to_dict('records'):
            cleaned = {k: nan_to_none(v) for k, v in record.items()}
            final_data.append(cleaned)

        logger.info(f"Prepared final records: {len(final_data)}")
        return final_data

    except Exception as e:
        logger.exception(f"Error in run_func: {e}")
        return []


def main():
    logger.info("=== Program started ===")

    try:
        result = run_func(
            '2025-06-01',
            '2025-06-11',
            os.path.join(JSON_DIR, 'fb_spend.json'),
            os.path.join(JSON_DIR, 'network_conv.json')
        )

        logger.info(f"Total records to upsert: {len(result)}")

        for row in result:
            try:
                logger.debug(f"Upserting record: {row}")
                upsert(row)
            except Exception as e:
                logger.exception(f"Error during upsert for record {row}: {e}")

        print(query_by_date(ISO_format('2025-06-04')))
        print('====================================')

        logger.info("=== Program finished successfully ===")

    except Exception as e:
        logger.exception(f"Unhandled error in main(): {e}")


if __name__ == '__main__':
    main()