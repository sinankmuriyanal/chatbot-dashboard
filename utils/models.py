from sqlalchemy import Column, Integer, String
from .main import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(String)
    bot_response = Column(String)