from fastapi import APIRouter

router = APIRouter()

@router.get("/goals")
def get_goals():
    return [{"title": "Workout"}]
