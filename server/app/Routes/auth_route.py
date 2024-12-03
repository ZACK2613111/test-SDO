from fastapi import APIRouter, HTTPException, Depends, Response, status, Request
from sqlalchemy.orm import Session
from app.DB.session import get_db
from app.DB.models import User
from app.Services.auth_service import register_user, authenticate_user, create_access_token, get_current_user
from app.Models.auth_model import LoginRequest
from app.Models.user_model import UserCreate
from starlette.responses import JSONResponse

router = APIRouter()

@router.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    try:
        new_user = register_user(db=db, email=user.email, password=user.password, name=user.name)
    except HTTPException as e:
        raise e  

    access_token = create_access_token(data={"sub": new_user.email, "id": new_user.id, "name": new_user.name})

    response = JSONResponse(
        content={
            "msg": "User registered and logged in successfully",
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
        },
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=3600)
    
    return response

@router.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=request.email, password=request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})

    response = JSONResponse(content={"msg": "Login successful", "user_id": user.id}, status_code=status.HTTP_200_OK)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=3600)
    
    return response

@router.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, email=request.email, password=request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})

    response = JSONResponse(content={"msg": "Login successful", "user_id": user.id}, status_code=status.HTTP_200_OK)
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=3600)
    
    return response

@router.post("/auth/logout")
def logout(response: Response, request: Request):
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    response.delete_cookie("access_token")
    
    return {"msg": "Logged out successfully"}