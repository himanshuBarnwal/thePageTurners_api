from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

host="sql12.freesqldatabase.com"
db_name= "sql12621685"
db_user="sql12621685"
db_password= "VHNXep4Ink"
Port="3306"

# SQLALCHAMY_DATABASE_URL = 'mysql+pymysql://root@localhost:3306/thepageturners'
SQLALCHAMY_DATABASE_URL = f'mysql+pymysql://{db_user}:{db_password}@{host}:{Port}/{db_name}'
engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()