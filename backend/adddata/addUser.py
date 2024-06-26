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

    User(username='user1', password=pwd_context.hash('user1'),electricity_meter='admin',confirm_email=True,daylimit =20,monthlimit=20),
    
]


session.add_all(new_users)


session.commit()


session.close()
