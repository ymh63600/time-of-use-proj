from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.security import HTTPBearer
from config import Config

security = HTTPBearer()
engine = create_engine(Config.DB_URL)
Session = sessionmaker(bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()