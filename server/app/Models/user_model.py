from pydantic import BaseModel, EmailStr, field_validator
from typing import List

class UserBase(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

    @field_validator("name")
    def validate_name_length(cls, value: str) -> str:
        if len(value.strip()) > 20:
            raise ValueError("Name cannot be longer than 20 characters.")
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        return value.strip()


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def validate_password_strength(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(c.isalpha() for c in value):
            raise ValueError("Password must contain at least one letter.")
        if not any(c in "!@#$%^&*()_+-=" for c in value):
            raise ValueError("Password must contain at least one special character.")
        if " " in value:
            raise ValueError("Password cannot contain spaces.")
        return value
    
    class Config:
        from_attributes = True


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
