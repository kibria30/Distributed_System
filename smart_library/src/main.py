from fastapi import FastAPI
from src.api import register_routers
from src.database import init_db
from pydantic import BaseModel
from src.users.service import get_total_user_count
from src.books.service import books_overview
from src.loans.service import loans_overview

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_db()

register_routers(app)


class StatsOverview(BaseModel):
    total_books: int
    total_users: int
    books_available: int 
    books_borrowed: int
    overdue_loans: int
    loans_today: int
    returns_today: int


@app.get("/stats/overview")
async def get_stats_overview():
    books_overview_data = await books_overview()
    loans_overview_data = await loans_overview()
    overview = StatsOverview(
        total_books=books_overview_data.total_books,
        total_users=await get_total_user_count(),
        books_available=books_overview_data.books_available,
        books_borrowed=books_overview_data.books_borrowed,
        overdue_loans=loans_overview_data.overdue_loans,
        loans_today=loans_overview_data.loans_today,
        returns_today=loans_overview_data.returns_today
    )
    return overview