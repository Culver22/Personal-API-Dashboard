from fastapi import APIRouter
from app.api import goals

router = APIRouter()

# Include each feature's router
router.include_router(goals.router)
