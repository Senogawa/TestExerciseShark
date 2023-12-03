from pyrogram import idle, filters
from loader import app, db, logger, UnixTimes
import asyncio
import handlers.users_handlers
import handlers.admin_handlers
import os
from random import randint



async def start_app():
    await app.start()
    await idle()
    await app.stop()

async def check_chat_history(user: dict):
    my_id = await app.get_me()
    my_id = my_id.id
    if user.state == "SS":
        return
    
    async for message in app.get_chat_history(user.user_id):
        try:
            if (message.from_user.id == my_id) and ("Хорошего дня" in message.text):
                await db.change_user_state_and_lmt(user.user_id, "SS", "0")
                logger.info(f"Отправлено оканчивающее сообщение, пользователь переведен в статус SS. Пользователь: {user.user_id} Статус: {user.state}")
                return
            
        except TypeError:
            continue
        
async def send_users_notifications():
    while True:
        users = await db.get_users()
        unix_now = UnixTimes.get_unix_now()

        for user in users:
            try:
                if user.state == "SS":
                    continue

                print(int(user.lmt) - unix_now)

                await check_chat_history(user)

                if (int(user.lmt) - unix_now) <= 0:
                    if (user.state == "HL"): #switch to MT
                        await app.send_message(user.user_id, "Добрый день! |TESTS!|") #TODO remove |tests| text
                        logger.info(f"Отправлено приветственное сообщение. Пользователь: {user.user_id} Статус: {user.state}")

                        await db.change_user_state_and_lmt(user.user_id, "MT", str(unix_now + 10)) #TODO change time

                    if user.state == "MT": #switch to MM
                        photos = os.listdir("./photos/")
                        if not photos:
                            await app.send_message(user.user_id, "Материала для Вас не нашлось! Вернусь к Вам позже! |TESTS!|")
                            logger.info(f"Отправлено сообщение без материала. Пользователь {user.user_id} Статус: {user.state}")

                            await db.change_user_state_and_lmt(user.user_id, "MT", str(unix_now + 60 * 5))
                            continue

                        await app.send_message(user.user_id, "MATERIAL! |TESTS!|")
                        await app.send_photo(user.user_id, f"./photos/{photos[randint(0, len(photos) - 1)]}")

                        logger.info(f"Отправлено сообщение с материалом. Пользователь {user.user_id} Статус: {user.state}")

                        await db.change_user_state_and_lmt(user.user_id, "MM", str(unix_now + 10)) #TODO CHANGE TIME


                    if user.state == "MM": #switch to SS
                        await app.send_message(user.user_id, "Скоро вернусь с новым материалом!")
                        logger.info(f"Отправлено сообщение без триггера. Пользователь: {user.user_id} Статус: {user.state}")

                        await db.change_user_state_and_lmt(user.user_id, "SS", "0")

            except ConnectionError:
                await asyncio.sleep(5)
                continue

        await asyncio.sleep(5)


async def main():
    tasks = [
        asyncio.create_task(send_users_notifications()),
        asyncio.create_task(start_app())
    ]
    await asyncio.gather(*tasks)






if __name__ == "__main__":
    app.run(main())