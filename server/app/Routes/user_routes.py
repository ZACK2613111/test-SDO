from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Services.user_service import create_user, get_user_by_email, fetch_user_by_id
from app.Models.user_model import User, UserCreate
from app.DB.session import get_db

router = APIRouter()

@router.post("/users/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user.name, user.email, user.password)

from app.Services.user_service import fetch_user_by_id  # Update the import

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = fetch_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

