from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.database import Base
from enum import Enum as PyEnum


class WorkoutType(str, PyEnum):
    running = "running"
    gym = "gym"
    cycling = "cycling"
    yoga = "yoga"
    other = "other"


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(WorkoutType), nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    sets = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
