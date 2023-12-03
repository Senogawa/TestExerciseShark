from pyrogram import filters
from loader import app, db, UnixTimes
from datetime import datetime
from pyrogram.handlers.message_handler import MessageHandler



@app.on_message(filters.all & ~filters.me)
async def register_handler(client, message):
    try:
        user_in_db = await db.check_user_in_db(str(message.from_user.id))

    except AttributeError:
        return
    
    if not user_in_db:
        unix_time = int(datetime.utcnow().timestamp())
        await db.add_user(str(message.from_user.id), str(unix_time + UnixTimes.min_10))
        print(f"Пользователь добавлен {message.from_user.id}")