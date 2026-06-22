from datetime import datetime
from typing import List
from typing import Any, Dict, Optional

# import SQL Alchemy
from sqlalchemy import String, Text, ForeignKey, func, Boolean
from sqlalchemy import BigInteger, DateTime, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

# import DB Base
from services.db_services.db_session import Base

# PG vector import
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB

# ==========================================================================================
# User Chat Tables 
# ==========================================================================================

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(127), default="New Chat")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # server_default= (which generates DEFAULT CURRENT_TIMESTAMP in your actual SQL DDL)
    messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )


class ChatMessage(Base):
    # Represents one message in a conversation.
    __tablename__ = "chat_messages"

    message_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_sessions.session_id", ondelete="CASCADE")
    )
    role: Mapped[str] = mapped_column(String(10))  # 'user' or 'assistant'
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Back reference to the parent conversation
    session: Mapped["ChatSession"] = relationship(back_populates="messages")


# ==========================================================================================
# User Login Details
# ==========================================================================================

class Users (Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(String(63), unique=True, nullable=False, index=True)
    user_password: Mapped[str] = mapped_column(String(255), nullable=False)
    user_email_id: Mapped[str] = mapped_column(String(63), unique=True, nullable=False, index=True)
    user_is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    user_last_login: Mapped[datetime] = mapped_column(server_default=func.now())
    user_created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __repr__(self):
        return f"<user name is {self.user_name !r} and user id is {self.user_id}>"
    