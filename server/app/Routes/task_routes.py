from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from app.Services.task_service import create_task, get_tasks_by_user, update_task, delete_task
from app.Models.task_model import TaskCreate, Task
from app.DB.session import get_db
from app.Services.auth_service import get_current_user

router = APIRouter()

@router.post("/tasks/", response_model=Task, summary="Create a new task", description="Create a new task for the authenticated user.")
def create_task_route(task: TaskCreate, request: Request, db: Session = Depends(get_db)):
    """
    This route allows the authenticated user to create a new task.
    
    - `title`: The title of the task (required).
    - `description`: An optional description for the task.
    - `is_completed`: A boolean indicating whether the task is completed or not (default is False).
    
    Returns the newly created task, including its ID and completion status.
    """
    user = get_current_user(db, request.cookies.get("access_token"))
    return create_task(db=db, title=task.title, description=task.description, is_completed=task.is_completed, user_id=user.id)


@router.put("/tasks/{task_id}", response_model=Task, summary="Update an existing task", description="Update an existing task by its ID.")
def update_task_route(task_id: int, task: TaskCreate, request: Request, db: Session = Depends(get_db)):
    """
    This route allows the authenticated user to update an existing task.
    
    - `task_id`: The ID of the task to be updated.
    - `title`: The new title for the task.
    - `description`: The new description for the task (optional).
    - `is_completed`: Whether the task is completed or not.
    
    Raises HTTP 404 if the task is not found or 403 if the task does not belong to the authenticated user.
    Returns the updated task.
    """
    user = get_current_user(db, request.cookies.get("access_token"))
    updated_task = update_task(db=db, task_id=task_id, title=task.title, description=task.description, is_completed=task.is_completed)
    
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if updated_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only update your own tasks")
    
    return updated_task


@router.delete("/tasks/{task_id}", response_model=Task, summary="Delete a task", description="Delete a task by its ID.")
def delete_task_route(task_id: int, request: Request, db: Session = Depends(get_db)):
    """
    This route allows the authenticated user to delete a task by its ID.
    
    - `task_id`: The ID of the task to be deleted.
    
    Raises HTTP 404 if the task is not found or 403 if the task does not belong to the authenticated user.
    Returns the deleted task.
    """
    user = get_current_user(db, request.cookies.get("access_token"))
    deleted_task = delete_task(db=db, task_id=task_id)
    
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if deleted_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own tasks")
    
    return deleted_task
