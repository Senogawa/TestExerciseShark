from configparser import ConfigParser
from dataclasses_cnf import *
from loguru import logger
from pyrogram import Client

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

app = Client("my_account", api_id = telegram_data.api_id, api_hash = telegram_data.api_hash)