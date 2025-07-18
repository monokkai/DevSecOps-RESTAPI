from sqlalchemy.orm import Session
from api import models
from typing import Optional


def create_user(db: Session, username: str, hashed_password: str, full_name: Optional[str] = None):
    user = models.User(username=username, full_name=full_name, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def update_user(db: Session, id: int, username: str, full_name: str, hashed_password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None

    user.username = username
    user.full_name = full_name
    user.hashed_password = hashed_password

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).delete()



