from pydantic import BaseModel, EmailStr, Field
from src.entities.user import UserRole


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole
    password: str

    