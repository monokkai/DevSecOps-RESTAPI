from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database connection parameters from environment variables
DB_HOST = os.getenv("DB_HOST", "mysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "users_db")

# Construct database URL
MYSQL_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

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
