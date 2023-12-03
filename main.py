from pyrogram import idle, filters
from loader import app, db, logger, UnixTimes
import asyncio
import handlers.users_handlers
import handlers.admin_handlers
from users_functions.send_notifications import send_users_notifications



async def start_app():
    await app.start()
    await idle()
    await app.stop()




async def main():
    tasks = [
        asyncio.create_task(send_users_notifications()),
        asyncio.create_task(start_app())
    ]
    await asyncio.gather(*tasks)






if __name__ == "__main__":
    app.run(main())