from sqlalchemy import Sequence, Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app import settings


Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    
    user_id_seq = Sequence("user_id_seq")
    id = Column(Integer, user_id_seq, server_default=user_id_seq.next_value(), primary_key=True)
    name = Column(String, nullable=False, index=True)
    account = Column(String, nullable=False, index=True, unique=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, index=True)
    token = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # def __init__(self, name, account, password):
    #     self.name = name
    #     self.account = account
    #     self.password = password

