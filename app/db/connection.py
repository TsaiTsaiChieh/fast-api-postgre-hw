import os
from sqlalchemy import schema, types, create_engine
from sqlalchemy.ext.declarative import declarative_base  
from app import settings
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# db_url = os.environ.get(settings.settings.database_url)
engine = create_engine(settings.settings.database_url)
# Base = declarative_base(engine)
# meta = Base.metadata
# 建立 Schema
Base.metadata.create_all(engine)  # 相當於 Create Table

Session = sessionmaker(bind=engine)
session = Session()