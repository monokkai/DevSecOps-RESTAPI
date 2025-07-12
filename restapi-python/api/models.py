from sqlalchemy import Column, Integer, String, Boolean
from database import base


class User(base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(50))
    hashed_password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)
