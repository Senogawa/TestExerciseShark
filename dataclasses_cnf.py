from dataclasses import dataclass

@dataclass
class TelegramData:
    api_id: str
    api_hash: str



@dataclass
class DatabaseData:
    username: str
    password: str
    database: str
    host: str
    port: int