from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base


class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    deadline = Column(String, nullable=True)
    completed = Column(Boolean, nullable=True)
