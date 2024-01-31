from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class ImageModel(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    file_hash = Column(String)
    path = Column(String)
    downloaded_at = Column(DateTime, default=datetime.datetime.utcnow)