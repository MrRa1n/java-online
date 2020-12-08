from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine('postgres://{}:{}@{}:{}/{}'.format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASS'),
    os.environ.get('DB_HOST'),
    os.environ.get('DB_PORT'),
    os.environ.get('DB_NAME')), echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()