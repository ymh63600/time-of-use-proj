from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from datetime import datetime
from pydantic import BaseModel

Base=declarative_base()

class Electricity_Data(Base):
    __tablename__='data_time'
    device_uuid = Column(sa.VARCHAR, primary_key=True)
    generated_time = Column(sa.types.DateTime, nullable=False)
    normal_usage = Column(sa.Float, nullable=True)

class User(Base):
    __tablename__='user_table'
    username=Column(sa.VARCHAR,primary_key=True)
    password=Column(sa.VARCHAR,nullable=False)
    electricity_meter=Column(sa.VARCHAR,nullable=False)
    confirm_email=Column(sa.BOOLEAN,default=False)
    creat_time=Column(sa.types.DateTime,default=datetime.utcnow())
    last_login=Column(sa.types.DateTime,nullable=True)

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class ForgetPassword(BaseModel):
    new_password: str
    confirm_password: str


