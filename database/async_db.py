from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from loader import database_data
from sqlalchemy import insert, select, update
from database.models import Users
import asyncio
from loguru import logger
from datetime import datetime
import time


class AsyncDatabase:

    def __init__(self):
        user = database_data.username
        password = database_data.password
        host = database_data.host
        database =database_data.database
        DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}/{database}"

        self.engine = create_async_engine(DATABASE_URL)
        self.async_session = sessionmaker(self.engine, class_= AsyncSession, expire_on_commit = False)



    
    async def add_user(self, user_id: int, timestamp: int):
        query = insert(Users).values(user_id = user_id, lmt = timestamp, state = "HL", register_time = int(datetime.utcnow().timestamp()))
        async with self.async_session() as session:
            await session.execute(query)
            await session.commit()


    async def get_users(self):
        query = select(Users)
        async with self.async_session() as session:
            result = await session.execute(query)

        return result.scalars().all()

    async def get_today_users(self):
        unix_now = int(datetime.utcnow().timestamp())
        today = time.strftime('%d', time.gmtime(unix_now))

        users = await self.get_users()
        users_added_today = list()
        for user in users:
            if time.strftime("%d", time.gmtime(user.register_time)) == today:
                users_added_today.append(user.user_id)

        return users_added_today

    async def change_user_state(self, user_id: int, state: str):
        query = update(Users).where(Users.user_id == user_id).values(state = state) 
        async with self.async_session() as session:
            await session.execute(query)
            await session.commit()

        




async def main():
    db = AsyncDatabase()
    await db.change_user_state(4443434, "KS")

if __name__ == "__main__":
    asyncio.run(main())