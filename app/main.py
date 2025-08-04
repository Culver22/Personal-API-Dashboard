from fastapi import FastAPI
from app.api import api_router

app = FastAPI()

# Mount the full API
app.include_router(api_router)
