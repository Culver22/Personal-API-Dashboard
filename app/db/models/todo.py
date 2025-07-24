from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.db.database import Base
from enum import Enum as PyEnum


class PriorityLevel(str, PyEnum):
    low = 'low'
    medium = 'medium'
    high = 'high'


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(Enum(PriorityLevel), nullable=True)
