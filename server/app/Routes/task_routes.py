from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.Services.task_service import create_task, get_tasks_by_user, update_task, delete_task
from app.Models.task_model import TaskCreate, Task
from app.DB.session import get_db
from app.Services.auth_service import get_current_user

router = APIRouter()
@router.post("/tasks/", response_model=Task)
def create_task_route(task: TaskCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(db, request.cookies.get("access_token"))
    return create_task(db=db, title=task.title, description=task.description, is_completed=task.is_completed, user_id=user.id)

@router.put("/tasks/{task_id}", response_model=Task)
def update_task_route(task_id: int, task: TaskCreate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(db, request.cookies.get("access_token"))
    updated_task = update_task(db=db, task_id=task_id, title=task.title, description=task.description, is_completed=task.is_completed)
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if updated_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only update your own tasks")
    
    return updated_task

@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task_route(task_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(db, request.cookies.get("access_token"))
    deleted_task = delete_task(db=db, task_id=task_id)
    
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if deleted_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own tasks")
    
    return deleted_task
