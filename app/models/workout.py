from pydantic import BaseModel
from typing import Optional
from enum import Enum


class WorkoutType(str, Enum):
    running = 'running'
    gym = 'gym'
    yoga = "yoga"
    other = "other"


class CreateWorkout(BaseModel):
    type: WorkoutType
    duration_minutes: Optional[int] = None  # Duration in minutes
    sets: Optional[int] = None  # For gym-style workouts
    notes: Optional[str] = None
    completed: Optional[bool] = False


class ReadWorkout(CreateWorkout):
    id: int