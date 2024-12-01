from app.DB.session import SessionLocal
from app.DB.models.user import User
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str :
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, name: str, email : str, password: str):
    hashed_password = hash_password(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_name(db: Session, name: str) -> User:
    return db.query(User).filter(User.name == name).first()

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def fetch_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, name: str, email: str, password: str):
    hashed_password = hash_password(password)
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user:
        db_user.name = name
        db_user.email = email
        db_user.password = hashed_password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return {"message": "User successfully deleted"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
