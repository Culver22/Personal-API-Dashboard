from pydantic import BaseModel, StrictBool
from typing import Optional


class CreateGoal(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    completed: Optional[StrictBool] = False


class ReadGoal(CreateGoal):
    id: int


class UpdateGoal(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[str] = None
    completed: Optional[bool] = None
