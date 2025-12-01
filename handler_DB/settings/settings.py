import os
import sys
from loguru import logger
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from handler_DB.models.models import Base
from CONFIG import JSON_DIR, LOGS_DIR

logger.add(sys.stderr, format="{time} {level} {message}",  level="INFO")
logger.add(os.path.join(LOGS_DIR, "db_settings_{time}.log"))

load_dotenv()

user_db = os.getenv('POSTGRES_USER', 'postgres')
pass_db = os.getenv('POSTGRES_PASSWORD', 'postgres')
# host_db = os.getenv('POSTGRES_HOST', 'localhost')
name_db = os.getenv('POSTGRES_DB', 'postgres')
# port_db = os.getenv('POSTGRES_PORT', 5432)

url = f'postgresql://{user_db}:{pass_db}@db:5432/{name_db}'
logger.info(f"Connecting to database: {url}")

try:
    engine = create_engine(url)
    logger.success("Database engine created successfully")
except Exception as e:
    logger.exception(f"Failed to create engine: {e}")
    raise

try:
    Base.metadata.create_all(bind=engine)
    logger.success("Database tables created or already exist")
except Exception as e:
    logger.exception(f"Failed to create tables: {e}")
    raise

try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.success("SessionLocal configured successfully")
except Exception as e:
    logger.exception(f"Failed to configure SessionLocal: {e}")
    raise
