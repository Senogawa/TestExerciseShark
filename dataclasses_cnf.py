from dataclasses import dataclass

@dataclass
class TelegramData:
    ...



@dataclass
class DatabaseData:
    username: str
    password: str
    database: str
    host: str