from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from datetime import datetime
from pydantic import BaseModel

Base=declarative_base()

class Electricity_Data(Base):
    __tablename__='data_time'
    device_uuid = Column(sa.VARCHAR, primary_key=False)
    generated_time = Column(sa.types.DateTime, nullable=False)
    normal_usage = Column(sa.Float, nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint('device_uuid', 'generated_time'),
    )

class User(Base):
    __tablename__='user_table'
    username=Column(sa.VARCHAR,primary_key=True)
    password=Column(sa.VARCHAR,nullable=False)
    electricity_meter=Column(sa.VARCHAR,nullable=False)
    confirm_email=Column(sa.BOOLEAN,default=False)
    creat_time=Column(sa.types.DateTime,default=datetime.utcnow())
    last_login=Column(sa.types.DateTime,nullable=True)
    daylimit=Column(sa.INT,nullable=True)
    monthlimit=Column(sa.INT,nullable=True)
    

class UpdatePassword(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str

class ForgetPassword(BaseModel):
    new_password: str
    confirm_password: str


