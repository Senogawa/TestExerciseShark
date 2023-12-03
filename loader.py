from configparser import ConfigParser
from dataclasses_cnf import *
from loguru import logger
from pyrogram import Client
from database.async_db import AsyncDatabase
from datetime import datetime


logger.add("logs.log")

config = ConfigParser()
config.read("./conf.ini")


telegram_data = TelegramData(
    config["TELEGRAM"]["api_id"],
    config["TELEGRAM"]["api_hash"]
)
database_data =DatabaseData(
    config["DATABASE"]["username"],
    config["DATABASE"]["password"],
    config["DATABASE"]["database"],
    config["DATABASE"]["host"],
    config["DATABASE"]["port"]
)

class UnixTimes:
    min_10 = 60 * 10
    min_90 = 60 * 90
    min_180 = 60 * 180

    def get_unix_now() -> int:
        return int(datetime.utcnow().timestamp())

app = Client("my_account", api_id = telegram_data.api_id, api_hash = telegram_data.api_hash)
db = AsyncDatabase(
    database_data.username,
    database_data.password,
    database_data.host,
    database_data.database
)

