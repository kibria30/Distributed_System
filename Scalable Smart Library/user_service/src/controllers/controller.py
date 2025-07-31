from fastapi import APIRouter, HTTPException
from src.models import models
from src.services import service
from fastapi import Depends


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

@router.post("/")
async def create_user(user: models.UserCreate):
   return await service.create_user(user.name, user.email, user.role, user.password)


@router.get("/{id}")
async def get_user(id: int):
    user = await service.get_user(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# @router.put("/{id}")
# async def update_user(id: int, user: models.UserUpdate):
#     updated_user = await service.update_user(id, user)
#     if updated_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return updated_user