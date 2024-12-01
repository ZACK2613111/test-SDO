from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Services.user_service import create_user, get_user_by_email, get_user_by_id, get_user_by_username

from app.DB.models.user import User

from app.DB.session import get_db

router = APIRouter()

@router.post("/users/", response_model=User)
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, username, email, password)

@router.get("/users/{user_id}", response_model=User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
