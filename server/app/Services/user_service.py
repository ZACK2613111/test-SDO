from sqlalchemy.orm import Session
from app.Models.user_model import User, UserCreate
from app.Services.auth_service import get_current_user
from fastapi import HTTPException

def create_user(db: Session, user_data: UserCreate) -> User:

    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def fetch_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if db_user:
        db_user.name = user_data.name
        db_user.email = user_data.email
        db_user.password = user_data.password 
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
