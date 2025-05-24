from fastapi import FastAPI
from src.api import register_routers
from src.database import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

register_routers(app)