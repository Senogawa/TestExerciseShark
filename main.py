from pyrogram import filters, idle
from loader import app
import asyncio



@app.on_message(filters.all)
async def echo(client, message):
    print("!!!")
    await message.reply_text("Если вы видите это сообщение, значит сейчас я занимаюсь разработкой и тестирую новое приложение. Не обращайте внимания на данное сообщение")



async def start_app():
    await app.start()
    await idle()
    await app.stop()

async def test():
    while True:
        print("!")
        await asyncio.sleep(1)

async def main():
    tasks = [
        asyncio.create_task(start_app()),
        asyncio.create_task(test())
    ]
    await asyncio.gather(*tasks)






if __name__ == "__main__":
    app.run(main())