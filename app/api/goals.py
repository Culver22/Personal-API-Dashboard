from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.goal import CreateGoal, ReadGoal
from app.db.models.goal import Goal
from app.db.database import get_db
from typing import List
from fastapi import HTTPException

router = APIRouter()


# Route to create a new goal and store it in the database
@router.post("/", response_model=ReadGoal)
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


@router.get("/", response_model=List[ReadGoal])  # Returns a list of goals in the format defined by ReadGoal (ID)
async def get_goals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal))  # Select * From goals
    goals = result.scalars().all()  # Just the Goal objects - ignores row metadata

    return goals


@router.delete("/{goal_id}", status_code=204)  # successfully deleted
async def delete_goal(goal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).where(Goal.id == goal_id))  # Search for specific goal by ID
    goal = result.scalars().first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    await db.delete(goal)
    await db.commit()
