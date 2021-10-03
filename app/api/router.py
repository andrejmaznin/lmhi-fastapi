from fastapi import APIRouter

from .routes import auth_sessions


api_router = APIRouter()
api_router.include_router(auth_sessions.router, tags=["users"])
