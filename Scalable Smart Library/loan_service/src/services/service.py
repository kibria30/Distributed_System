from fastapi import HTTPException
from sqlalchemy.future import select
from src.entities.loan import Loan
from src.models.models import LoanPerUserResponse, BookDetails, UserDetails, LoanPerIdResponse
# from src.services import get_user
from src.database.session import get_db
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from src.entities.loan import LoanStatus
from .externalService import get_book, get_user, update_book

async def issue_book(user_id, book_id, due_date):
    #check if the user exists
    user = await get_user(user_id)
    print("from service user: ", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the book is available
    book = await get_book(book_id)
    print("from service book: ", book)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    elif book["available_copies"] <= 0:
        raise HTTPException(status_code=400, detail="Book not available")

    new_loan = Loan(user_id=user_id, book_id=book_id, due_date=due_date)

    async with get_db() as db:
        await update_book(book_id, book["copies"], book["available_copies"] - 1)
        db.add(new_loan)
        await db.commit()
        await db.refresh(new_loan)
    return new_loan



async def return_book(loan_id):
    async with get_db() as db:
        # Check if the loan exists
        loan = await db.execute(select(Loan).where(Loan.id == loan_id))
        loan = loan.scalars().first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if loan.status == LoanStatus.RETURNED:  # Here LoadStatus is must to added for checking
            raise HTTPException(status_code=400, detail="Loan already returned")
    
    loan.status = LoanStatus.RETURNED
    loan.return_date = datetime.now(timezone.utc)

    book = await get_book(loan.book_id)

    async with get_db() as db:
        db.add(loan)
        await db.commit()
        await db.refresh(loan)
        await update_book(book["id"], book["copies"], book["available_copies"] + 1)
        return loan



async def get_loan_history(user_id):
    async with get_db() as db:
        loan_history = await db.execute(
            select(Loan).where(Loan.user_id == user_id)
        )
        loan_history = loan_history.scalars().all()
        if len(loan_history) <= 0:
            raise HTTPException(status_code=404, detail="No loans found")
        
        loan_history_with_books = []
        for loan in loan_history:
            book = await get_book(loan.book_id)
            if book:
                loan_history_with_books.append(LoanPerUserResponse(
                    id=loan.id, 
                    book=BookDetails(
                        id=book["id"],
                        title=book["title"],
                        author=book["author"]
                    ),
                    issue_date=loan.issue_date,
                    due_date=loan.due_date,
                    return_date=loan.return_date,
                    status=loan.status
                ))
            else:
                raise HTTPException(status_code=404, detail="Book not found")

    return loan_history_with_books


async def get_loan_by_id(loan_id):
    async with get_db() as db:
        loan = await db.execute(select(Loan).where(Loan.id == loan_id))
        loan = loan.scalars().first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        
        usere = await get_user(loan.user_id)
        if not usere:
            raise HTTPException(status_code=404, detail="User not found")
        
        book = await get_book(loan.book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        return LoanPerIdResponse(
            id=loan.id,
            user=UserDetails(
                id=usere["id"],
                name=usere["name"],
                email=usere["email"]
            ),
            book=BookDetails(
                id=book["id"],
                title=book["title"],
                author=book["author"]
            ),
            issue_date=loan.issue_date,
            due_date=loan.due_date,
            return_date=loan.return_date,
            status=loan.status
        )