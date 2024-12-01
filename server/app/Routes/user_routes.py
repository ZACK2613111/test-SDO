from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.Services.user_service import create_user, get_user_by_email, fetch_user_by_id, update_user, hash_password, delete_user, get_all_users
from app.Models.user_model import User, UserCreate
from app.DB.session import get_db

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = fetch_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[User])
def get_all_users_route(db: Session = Depends(get_db)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

@router.post("/users/", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user.name, user.email, user.password)

@router.put("/users/{user_id}", response_model=User)
def update_user_route(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = fetch_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = hash_password(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=dict)
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
