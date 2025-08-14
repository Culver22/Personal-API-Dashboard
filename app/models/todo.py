from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Priority(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class CreateTodo(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[Priority] = Priority.medium  # Set default value to medium


class ReadTodo(CreateTodo):
    id: int


class UpdateTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
