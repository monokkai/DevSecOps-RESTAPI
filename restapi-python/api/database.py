from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database URL from environment variable or use default
MYSQL_DATABASE_URL = os.getenv(
    "MYSQL_DATABASE_URL", 
    "mysql+pymysql://root:root@mysql:3306/users-db"
)

# Used for works with DB connections and makes SQL-requests
engine = create_engine(MYSQL_DATABASE_URL)
# Work with sessions in DB: No auto save chngs, No auto sending, The engine of DB
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ORM model creating. All of the models will be created from base class
base = declarative_base()

def get_db():
    # Object of the session
    db = session_local()
    try:
        # Returning the session to FastAPI(Where Depends is)
        yield db
    finally:
        db.close()
