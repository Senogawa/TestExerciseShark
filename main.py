from pyrogram import idle
from loader import app, db
import asyncio
import handlers.users_handlers
import handlers.admin_handlers


async def start_app():
    await app.start()
    await idle()
    await app.stop()

async def send_users_notifications():
    ...


async def main():
    tasks = [
        asyncio.create_task(start_app())
        #asyncio.create_task(test())
    ]
    await asyncio.gather(*tasks)






if __name__ == "__main__":
    app.run(main())