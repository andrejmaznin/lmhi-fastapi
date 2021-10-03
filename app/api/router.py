from fastapi import APIRouter

from .routes import users_routes


api_router = APIRouter()
api_router.include_router(users_routes.router, tags=["users"])
