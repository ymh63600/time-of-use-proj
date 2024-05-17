from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
sys.path.append("..")
from models import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

engine = create_engine('postgresql://admin:admin@localhost:5432/admin')


Session = sessionmaker(bind=engine)
session = Session()


new_users = [

    User(username='user3', password=pwd_context.hash('user3'),electricity_meter='admin',confirm_email=True,daylimit =20,monthlimit=20),
    #User(username='HI', password=pwd_context.hash('123'),electricity_meter='test')
    #User(username='Andy', password='6177321eac992341d1ad0823a07e76bfc4ee6909db120e377ea303fdc216756c'),
    #User(username='Cindy', password='002340b41aee7da76f4201bf18776291a812f796e20678c563b77b5b6c47c8a1')
]


session.add_all(new_users)


session.commit()


session.close()
