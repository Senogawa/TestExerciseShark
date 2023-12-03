from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, select, update
from database.models import Users
import asyncio
from datetime import datetime
import time



class AsyncDatabase:
    def __init__(self, user: str, password: str, host: str, database: str):
        DATABASE_URL = f"postgresql+asyncpg://{user}:{password}@{host}/{database}"

        self.engine = create_async_engine(DATABASE_URL)
        self.async_session = sessionmaker(self.engine, class_= AsyncSession, expire_on_commit = False)

    async def add_user(self, user_id: str, timestamp: str):
        query = insert(Users).values(user_id = user_id, lmt = timestamp, state = "HL", register_time = str(int(datetime.utcnow().timestamp())))
        async with self.async_session() as session:
            await session.execute(query)
            await session.commit()


    async def get_users(self) -> list:
        query = select(Users)
        async with self.async_session() as session:
            result = await session.execute(query)

        return result.scalars().all()

    async def get_today_users(self) -> list:
        unix_now = int(datetime.utcnow().timestamp())
        today = time.strftime('%d', time.gmtime(unix_now))

        users = await self.get_users()
        users_added_today = list()
        for user in users:
            if time.strftime("%d", time.gmtime(int(user.register_time))) == today:
                users_added_today.append(user.user_id)

        return users_added_today

    async def change_user_state_and_lmt(self, user_id: str, state: str, lmt: str):
        query = update(Users).where(Users.user_id == user_id).values(state = state, lmt = lmt) 
        async with self.async_session() as session:
            await session.execute(query)
            await session.commit()

    async def check_user_in_db(self, user_id: str):
        query = select(Users).where(Users.user_id == user_id)
        async with self.async_session() as session:
            result = await session.execute(query)

        if len(result.scalars().all()):
            return True
        
        return False

        




async def main():
    db = AsyncDatabase()
    #await db.change_user_state(4443434, "KS")
    res = await db.check_user_in_db(43443434)
    print(res)

if __name__ == "__main__":
    asyncio.run(main())