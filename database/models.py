from sqlalchemy import Integer, String, Column, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    registered_at = Column(DateTime, default=func.now())

    messages = relationship("MessageLog", back_populates="user")

class MessageLog(Base):
    __tablename__ = "message_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message_text = Column(String)
    timestamp = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="messages")
