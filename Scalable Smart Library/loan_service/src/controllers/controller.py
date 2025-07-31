from fastapi import APIRouter, Depends, HTTPException
from src.models.models import GetLoan
from src.database.session import get_db
from src.services import service


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



@router.get("/{user_id}")
async def get_loan_history(user_id: int):
    loans = await service.get_loan_history(user_id)
    if not loans:
        raise HTTPException(status_code=404, detail="No loans found")
    return loans


@router.get("/{id}/")
async def get_loan_by_id(id: int):
    loan = await service.get_loan_by_id(id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan