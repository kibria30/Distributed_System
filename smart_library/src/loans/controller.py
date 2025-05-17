from fastapi import APIRouter, Depends, HTTPException
from .models import GetLoan
from src.database.session import get_db
from . import service


router = APIRouter(
    prefix="/api/v1/loans",
    tags=["Loans"],
)


@router.post("/")
async def issue_book(loan: GetLoan):
    loan = await service.issue_book(loan.user_id, loan.book_id, loan.due_date)
    return loan
   


@router.post("/returns")
async def return_book(loan_id: int):
    return await service.return_book(loan_id)


@router.get("/overdue")        # eita get(/{user_id}) er pore dile jamela hoy
async def get_overdue_loans():
    return await service.get_overdue_loans()


@router.get("/{user_id}")
async def get_loan_history(user_id: int):
    loans = await service.get_loan_history(user_id)
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found")
    return loans


@router.get("/{id}/extend")
async def extend_loan(id: int, days: int):
    return await service.extend_loan(id, days)


@router.get("/stats/users/active")
async def get_most_active_users():
    active_users = await service.get_most_active_users()
    if len(active_users) <= 0:
        raise HTTPException(status_code=404, detail="No active users found")
    return active_users