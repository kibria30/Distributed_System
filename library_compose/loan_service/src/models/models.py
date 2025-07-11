from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class GetLoan(BaseModel):
    user_id : int
    book_id : int
    due_date : datetime


class BookDetails(BaseModel):
    id: int
    title: str
    author: str

class LoanPerUserResponse(BaseModel):
    id: int
    book: BookDetails
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: str


class UserDetails(BaseModel): 
    id: int
    name: str
    email: str


class LoanPerIdResponse(BaseModel):
    id: int
    user: UserDetails
    book: BookDetails
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime]
    status: str