from pydantic import BaseModel, field_validator
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    @field_validator('is_completed')
    def check_is_completed(cls, value):
        if not isinstance(value, bool):
            raise ValueError('is_completed must be a boolean value (True or False)')
        return value

    @field_validator('title')
    def title_length_check(cls, value):
        if len(value) < 3:
            raise ValueError('Title must be at least 3 characters long')
        if len(value) > 100:
            raise ValueError('Title must be less than 100 characters long')
        return value

    @field_validator('description')
    def description_length_check(cls, value):
        if value and len(value) > 255:
            raise ValueError('Description must be less than 255 characters long')
        return value

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
