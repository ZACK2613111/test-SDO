from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.Services.task_service import create_task, get_tasks_by_user, update_task, delete_task
from app.Models.task_model import TaskCreate, Task
from app.DB.session import get_db

router = APIRouter()

@router.post("/tasks/", response_model=Task)
def create_task_route(task: TaskCreate, db: Session = Depends(get_db)):
    # The user id is required, and in most cases it should be from the authenticated user
    user_id = 1  
    return create_task(db=db, title=task.title, description=task.description, is_completed=task.is_completed, user_id=user_id)

@router.get("/tasks/{user_id}", response_model=List[Task])
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = get_tasks_by_user(db=db, user_id=user_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this user")
    return tasks

@router.put("/tasks/{task_id}", response_model=Task)
def update_task_route(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = update_task(db=db, task_id=task_id, title=task.title, description=task.description, is_completed=task.is_completed)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task_route(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task(db=db, task_id=task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task
