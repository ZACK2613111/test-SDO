import os
import re
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from typing import Optional
from app.DB.models import User
from sqlalchemy.orm import Session
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register_user(db: Session, email: str, password: str, name: str) -> User:
    if not validate_password(password):
        raise HTTPException(status_code=400, detail="Password does not meet complexity requirements")
    
    hashed_password = hash_password(password)
    db_user = User(email=email, password=hashed_password, name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    db_user = db.query(User).filter(User.email == email).first()
    if db_user and verify_password(password, db_user.password):
        return db_user
    return None

def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  
        return False
    if not re.search(r"[a-z]", password):  
        return False
    if not re.search(r"[0-9]", password):  
        return False
    if not re.search(r"[\W_]", password):  
        return False
    return True
