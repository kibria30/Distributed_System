from src.database.session import get_db
from src.entities.user import User
from sqlalchemy.future import select
from sqlalchemy import func


async def create_user(name, email, role, password):
    user = User(name=name, email=email, role=role, password=password)

    async with get_db() as db:
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user



async def get_user(id: int):
    
    async with get_db() as db:
        user = await db.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        if not user:
            return None
        return user


async def update_user(id: int, user_data):
    async with get_db() as db:
        user = await db.execute(select(User).where(User.id == id))
        user = user.scalars().first()
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
    return user

async def get_total_user_count():
    async with get_db() as db:
        total_users = await db.execute(select(func.count(User.id)))
        total_users = total_users.scalar()
        return total_users