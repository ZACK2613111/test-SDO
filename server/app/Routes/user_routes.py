from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.Services.user_service import create_user, get_user_by_email, fetch_user_by_id, update_user, delete_user, get_all_users
from app.Models.user_model import UserCreate, User
from app.DB.session import get_db
from app.Services.auth_service import get_current_user

router = APIRouter()
@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, request: Request = None, db: Session = Depends(get_db)):
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission for this!")
    
    db_user = fetch_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/", response_model=List[User])
def get_all_users_route(request: Request = None, db: Session = Depends(get_db)):
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users


@router.post("/users/", response_model=User)
def register_user(user: UserCreate, request: Request = None, db: Session = Depends(get_db)):
    current_user = get_current_user(db, request.cookies.get("access_token"))
    if current_user:
        raise HTTPException(status_code=400, detail="You are already logged in")

    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return create_user(db, user)

@router.delete("/users/{user_id}", response_model=dict)
def delete_user_route(user_id: int, request: Request = None, db: Session = Depends(get_db)):
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission for this!")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"msg": "User deleted successfully"}

@router.put("/users/{user_id}", response_model=User)
def update_user_route(user_id: int, user_data: UserCreate, request: Request = None, db: Session = Depends(get_db)):
    current_user = get_current_user(db, request.cookies.get("access_token"))
    
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="You don't have permission for this!")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.name = user_data.name
    db_user.email = user_data.email

    if user_data.password:
        db_user.password = user_data.password 

    db.commit()
    db.refresh(db_user)
    return db_user
