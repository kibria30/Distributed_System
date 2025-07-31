from fastapi import FastAPI
from src.controllers.controller import router as loans_router

def register_routers(app: FastAPI):
    app.include_router(loans_router)