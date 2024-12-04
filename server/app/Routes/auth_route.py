from fastapi import APIRouter, HTTPException, Depends, status, Request, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.DB.session import get_db
from app.DB.models import User
from app.Services.auth_service import (
    register_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.Models.auth_model import LoginRequest
from app.Models.user_model import UserCreate
from datetime import timedelta
import os

ACCESS_TOKEN_EXPIRE_MINUTES = 60
router = APIRouter()

def set_token_cookie(response: Response, token: str):
    """
    Set the access token as a cookie in the response.

    Args:
        response: The FastAPI response object.
        token: The JWT token to be set as a cookie.
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, response: Response, db: Session = Depends(get_db)):
    """
    Register a new user and automatically log them in.

    Args:
        user: UserCreate model containing user details for registration.
        response: The FastAPI response object to set the cookie.
        db: Database session dependency.

    Returns:
        A dictionary with success message and access token.
    """
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    try:
        new_user = register_user(
            db=db, email=user.email, password=user.password, name=user.name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    access_token = create_access_token(
        data={"sub": new_user.email, "id": new_user.id, "name": new_user.name},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    set_token_cookie(response, access_token)

    return {
        "msg": "User registered successfully and logged in.",
        "access_token": access_token,
    }


@router.post("/auth/login", status_code=status.HTTP_200_OK)
def login(request: Request, login_request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    """
    Log in an existing user and return an access token.

    Args:
        request: The incoming HTTP request to check for existing tokens.
        login_request: LoginRequest model containing user credentials.
        response: The FastAPI response object to set the cookie.
        db: Database session dependency.

    Returns:
        A dictionary with success message, access token, and token expiration.
    """
    token = request.cookies.get("access_token")
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    remaining_time = expiration_time - datetime.utcnow()
    
    if token:
        try:
            current_user = get_current_user(db, token)
            return {
                "msg": "Already logged in, you're not allowed to log in again until you log out.",
                "user": {
                    "id": current_user.id,
                    "name": current_user.name,
                    "email": current_user.email,
                },
            }
        except HTTPException:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = authenticate_user(db=db, email=login_request.email, password=login_request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    set_token_cookie(response, access_token)

    return {
        "msg": "Login successful",
        "access_token": access_token,
        "expires_in": remaining_time.total_seconds(),
    }
    
@router.post("/auth/logout", status_code=status.HTTP_200_OK)
def logout(request: Request, response: Response):
    """
    Log out the user by deleting the access token cookie.

    Args:
        request: The incoming HTTP request to read cookies.
        response: The FastAPI response object to delete the cookie.

    Returns:
        A dictionary with success message.
    """
    response.delete_cookie("access_token", path="/", samesite="lax")
    
    if "Authorization" in request.headers:
        del request.headers["Authorization"]
    
    if "access_token" not in request.cookies:
        raise HTTPException(status_code=401, detail="You're not logged in, please login")

    return {"msg": "Logged out successfully"}

@router.get("/auth/me", status_code=status.HTTP_200_OK)
def me(request: Request, db: Session = Depends(get_db)):
    """
    Get the current user's profile based on the access token.

    Args:
        request: The incoming HTTP request to check cookies.
        db: Database session dependency.

    Returns:
        A dictionary with user details (id, name, email).
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        current_user = get_current_user(db, token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
