from fastapi import FastAPI

from app.api.router import api_router
from app.db import db_session


def get_app() -> FastAPI:
    fast_app = FastAPI()
    fast_app.include_router(api_router)
    return fast_app


db_session.global_init("lmhi")
app = get_app()
