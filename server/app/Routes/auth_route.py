# app/Routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from app.DB.session import get_db
from app.DB.models import User
from app.Services.auth_service import register_user, authenticate_user, create_access_token
from app.Models.auth_model import LoginRequest

router = APIRouter()

@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = register_user(db=db, email=email, password=password, name=name)
    return {"msg": "User registered successfully", "email": user.email}

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=request.email, password=request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    response = Response(content="Login successful", status_code=status.HTTP_200_OK)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=3600)
    return response

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"msg": "Logged out successfully"}
