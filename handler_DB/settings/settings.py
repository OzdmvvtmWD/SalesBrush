
import os
from loguru import logger
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from handler_DB.models.models import Base

load_dotenv()

user_db = os.getenv('POSTGRES_USER', 'postgres')
pass_db = os.getenv('POSTGRES_PASSWORD', 'postgres')
host_db = os.getenv('POSTGRES_HOST', 'localhost')
name_db = os.getenv('POSTGRES_DB', 'postgres')
port_db = os.getenv('POSTGRES_PORT', 5432)

url = f'postgresql://{user_db}:{pass_db}@{host_db}:{port_db}/{name_db}'
print(url)
engine = create_engine(url)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
