from fastapi import APIRouter

from app.api.goals import router as goals_router
from app.api.todos import router as todos_router
from app.api.workouts import router as workouts_router

api_router = APIRouter()

# Include each router with a base path
api_router.include_router(goals_router, prefix="/goals", tags=["Goals"])
api_router.include_router(todos_router, prefix="/todos", tags=["Todos"])
api_router.include_router(workouts_router, prefix="/workouts", tags=["Workouts"])
