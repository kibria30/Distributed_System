from fastapi import FastAPI
from src.controllers.controller import router as users_router


def register_routers(app: FastAPI):
    app.include_router(users_router)
