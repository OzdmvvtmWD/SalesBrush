import os
import sys
from handler_DB.settings.settings import SessionLocal
from handler_DB.models.models import DailyStats
from sqlalchemy.dialects.postgresql import insert
from loguru import logger
from CONFIG import JSON_DIR, LOGS_DIR

logger.add(sys.stderr, format="{time} {level} {message}",  level="INFO")
logger.add(os.path.join(LOGS_DIR, "db_operations_{time}.log"))

def create_in_db(data: dict):
    logger.debug(f"Creating record in DB: {data}")

    try:
        db = SessionLocal()
        daily_stats = DailyStats(
            date=data.get('date'),
            campaign_id=data.get('campaign_id'),
            spend=data.get('spend'),
            conversions=data.get('conversions'),
            CPA=data.get('CPA'),
        )

        db.merge(daily_stats)
        db.commit()

        logger.info(
            f"Record inserted/merged successfully "
            f"[date={data.get('date')}, campaign_id={data.get('campaign_id')}]"
        )

    except Exception as e:
        logger.exception(
            f"Failed to create record in DB: {data} — {e}"
        )


def upsert(data: dict):
    logger.debug(f"Upsert called with data: {data}")

    try:
        db = SessionLocal()

        stmt = insert(DailyStats).values(data)
        stmt = stmt.on_conflict_do_update(
            index_elements=['date', 'campaign_id'],
            set_={
                'spend': stmt.excluded.spend,
                'conversions': stmt.excluded.conversions
            }
        )

        db.execute(stmt)
        db.commit()

        logger.info(
            f"Upsert successful "
            f"[date={data.get('date')}, campaign_id={data.get('campaign_id')}]"
        )

    except Exception as e:
        logger.exception(
            f"Upsert failed for data: {data} — {e}"
        )
