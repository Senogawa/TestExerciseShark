from configparser import ConfigParser
from dataclasses_cnf import *

config = ConfigParser()
config.read("./conf.ini")


telegram_data = TelegramData()
database_data =DatabaseData(
    config["DATABASE"]["username"],
    config["DATABASE"]["password"],
    config["DATABASE"]["database"],
    config["DATABASE"]["host"]
)