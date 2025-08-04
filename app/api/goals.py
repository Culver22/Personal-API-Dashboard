from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.goal import CreateGoal, ReadGoal
from app.db.models.goal import Goal
from app.db.database import get_db

router = APIRouter()


# Route to create a new goal and store it in the database
@router.post("/goals", response_model=ReadGoal)
async def create_goal(goal: CreateGoal, db: AsyncSession = Depends(get_db)):
    # Create a new SQLAlchemy goal instance from Pydantic input
    new_goal = Goal(
        title=goal.title,
        description=goal.description,
        deadline=goal.deadline,
        completed=goal.completed
    )

    db.add(new_goal)
    await db.commit()
    await db.refresh(new_goal)  # Refresh in order to get generated fields (e.g. ID)

    return new_goal
