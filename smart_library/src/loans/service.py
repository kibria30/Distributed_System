from fastapi import HTTPException
from sqlalchemy.future import select
from src.entities.loan import Loan
from .models import LoanPerUserResponse, BookDetails, OverdueLoansResponse, LoanExtensionResponse, UserDetails, MostACtiveUsersResponse,  LoanOverviewResponse
from src.users.service import get_user
from src.books.service import get_book, update_book, update_borrowed_count
from src.database.session import get_db
from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from src.entities.loan import LoanStatus

async def issue_book(user_id, book_id, due_date):
    #check if the user exists
    user = await get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the book is available
    book = await get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    elif book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    
    new_loan = Loan(user_id=user_id, book_id=book_id, due_date=due_date)

    async with get_db() as db:
        # Update the book's available copies
        await update_book(book_id, book.copies, book.available_copies - 1)
        await update_borrowed_count(book_id)
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
        await update_book(book.id, book.copies, book.available_copies + 1)
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
                        id=book.id,
                        title=book.title,
                        author=book.author
                    ),
                    issue_date=loan.issue_date,
                    due_date=loan.due_date,
                    return_date=loan.return_date,
                    status=loan.status
                ))
            else:
                raise HTTPException(status_code=404, detail="Book not found")

    return loan_history_with_books


async def get_overdue_loans():
    async with get_db() as db:
        overdue_loans = await db.execute(
            select(Loan).where(
                func.date(func.now()) > func.date(Loan.due_date), 
                Loan.status != "RETURNED"
            )
        )
        overdue_loans = overdue_loans.scalars().all()
        if len(overdue_loans) <= 0:
            raise HTTPException(status_code=404, detail="No overdue loans found")
        
        overdue_loans_with_books = []
        for loan in overdue_loans:
            user = await get_user(loan.user_id)
            book = await get_book(loan.book_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            elif not book:
                raise HTTPException(status_code=404, detail="Book not found")
            else:
                overdue_loans_with_books.append(OverdueLoansResponse(
                    id=loan.id, 
                    user=UserDetails(
                        id=user.id,
                        name=user.name,
                        email=user.email
                    ),
                    book=BookDetails(
                        id=book.id,
                        title=book.title,
                        author=book.author
                    ),
                    issue_date=loan.issue_date,
                    due_date=loan.due_date,
                    days_overdue=(datetime.now(timezone.utc) - loan.due_date).days
                ))

    return overdue_loans_with_books


async def extend_loan(loan_id, days):
    async with get_db() as db:
        # Check if the loan exists
        loan = await db.execute(select(Loan).where(Loan.id == loan_id))
        loan = loan.scalars().first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        if loan.status == LoanStatus.RETURNED:  # Here LoadStatus is must to added for checking
            raise HTTPException(status_code=400, detail="Loan already returned")
        
    due_date = loan.due_date   
    loan.due_date += timedelta(days=days)
    loan.extension_count += 1

    async with get_db() as db:
        db.add(loan)
        await db.commit()
        await db.refresh(loan)
    return LoanExtensionResponse(
        id=loan.id,
        user_id=loan.user_id,
        book_id=loan.book_id,
        issue_date=loan.issue_date,
        original_due_date=due_date,
        extended_due_date=loan.due_date,
        return_date=loan.return_date,
        status=loan.status,
        extension_count=loan.extension_count
    )


async def get_most_active_users():
    async with get_db() as db:
        most_active_users = await db.execute(
            select(Loan.user_id, func.count(Loan.id).label("loan_count"))
            .group_by(Loan.user_id)
            .order_by(func.count(Loan.id).desc())
            .limit(5)
        )
        most_active_users = most_active_users.all()
        if len(most_active_users) <= 0:
            raise HTTPException(status_code=404, detail="No active users found")
        
        most_active_users_with_details = []
        for user in most_active_users:
            user_details = await get_user(user[0])
            if not user_details:
                raise HTTPException(status_code=404, detail="User not found")
            else:
                most_active_users_with_details.append(MostACtiveUsersResponse(
                    user=UserDetails(
                        id=user_details.id,
                        name=user_details.name,
                        email=user_details.email
                    ),
                    total_loans=user[1]
                ))

    return most_active_users_with_details


async def loans_overview():
    async with get_db() as db:
        
        total_overdue_loans = len(await get_overdue_loans())

        loans_today = await db.execute(
            select(func.count(Loan.id)).where(
                func.date(Loan.issue_date) == func.date(func.now())
            )
        )
        loans_today = loans_today.scalar()

        returns_today = await db.execute(
            select(func.count(Loan.id)).where(
                func.date(Loan.return_date) == func.date(func.now())
            )
        )
        returns_today = returns_today.scalar()

    return LoanOverviewResponse(
        overdue_loans=total_overdue_loans,
        loans_today=loans_today,
        returns_today=returns_today
    )