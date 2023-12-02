from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR

base = declarative_base()

class Users(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    user_id = Column(String, unique = True)
    lmt = Column(String)
    state = Column(String)
    register_time = Column(String)