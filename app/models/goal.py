from pydantic import BaseModel
from typing import Optional


class CreateGoal(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[str] = None
    completed: Optional[bool] = False


class ReadGoal(CreateGoal):
    id: int
