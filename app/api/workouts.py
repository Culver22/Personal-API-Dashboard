from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.workout import CreateWorkout, ReadWorkout
from app.db.models.workout import Workout
from app.db.database import get_db

router = APIRouter()


# Route to create a new workout and store it in the database
@router.post("/workouts", response_model=ReadWorkout)
async def create_workout(workout: CreateWorkout, db: AsyncSession = Depends(get_db)):
    # Create a new SQLAlchemy Workout instance from Pydantic input
    new_workout = Workout(
        workout_type=workout.workout_type,
        duration_minutes=workout.duration_minutes,
        sets=workout.sets,
        notes=workout.notes,
        completed=workout.completed
    )

    db.add(new_workout)
    await db.commit()
    await db.refresh(new_workout)  # Refresh to get generated fields (e.g. ID)

    return new_workout


@router.get("/workouts", response_model=List[ReadWorkout])  # Returns a list of workouts from the database
async def get_workouts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workout))  # SELECT * FROM workouts
    workouts = result.scalars().all()
    return workouts


@router.delete("/workouts/{workout_id}", status_code=204)
async def delete_workout(workout_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Workout).where(Workout.id == workout_id))
    workout = result.scalars().first()

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    await db.delete(workout)
    await db.commit()
