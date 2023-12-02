from pyrogram import filters
from loader import app, db


@app.on_message(filters.command("users_today") & filters.me, 1)
async def users_added_today_handler(client, message):
    users_added_today = await db.get_today_users()
    text = "Пользователи добавленные сегодня:\n"
    if not len(users_added_today):
        await message.reply("Ни один пользователь не был добавлен сегодня!")
        return
    
    for user in users_added_today:
        text += f"{user}\n"

    await message.reply(text)
