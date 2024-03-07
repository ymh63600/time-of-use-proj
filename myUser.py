from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from datetime import datetime

Base=declarative_base()

class User(Base):
        __tablename__='user_table'
        username=Column(sa.VARCHAR,primary_key=True)
        password=Column(sa.VARCHAR,nullable=False)
        electricity_meter=Column(sa.VARCHAR,nullable=False)
        confirm_email=Column(sa.BOOLEAN,default=False)
        creat_time=Column(sa.types.DateTime,default=datetime.utcnow())
        last_login=Column(sa.types.DateTime,nullable=True)