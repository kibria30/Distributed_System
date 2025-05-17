from fastapi import APIRouter, HTTPException
from .models import UserCreate
from . import service
from fastapi import Depends


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

@router.post("/")
async def create_user(user: UserCreate):
   return await service.create_user(user.name, user.email, user.role, user.password)


@router.get("/{id}")
async def get_user(id: int):
    user = await service.get_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user