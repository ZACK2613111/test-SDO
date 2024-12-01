from app.DB.models.task import Task
from sqlalchemy.orm import Session
from app.Models.task_model import TaskCreate

def create_task(db: Session, title: str, description: str, is_completed: bool, user_id: int):
    new_task = Task(
        title=title,
        description=description,
        is_completed=is_completed,
        user_id=user_id
    )
    
    db.add(new_task)
    db.commit()
    
    db.refresh(new_task)
    
    return new_task

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()
     

def update_task(db: Session, task_id: int, title: str, description: str, is_completed: bool):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if task:
        task.title = title
        task.description = description
        task.is_completed = is_completed
        
        db.commit()
        db.refresh(task)
        
        return task
    else:
        return None 

def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if task:
        db.delete(task)
        db.commit()
        return task
    else:
        return None
