from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.DB.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False) 

    tasks = relationship("Task", back_populates="user")
