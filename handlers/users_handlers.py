from pyrogram import filters
from loader import app, logger, db
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
        await db.add_user(str(message.from_user.id), str(unix_time + 30)) #TODO change time
        print(f"Пользователь добавлен {message.from_user.id}")


@app.on_message(filters.me, 2)
async def stop_spamming(client, message):
    if "Хорошего дня" in message.text:
        await db.change_user_state_and_lmt(str(message.chat.id), "SS", "0")
        logger.info(f"Пользователь {message.chat.id} переведен в статус SS (Stop spaming)")