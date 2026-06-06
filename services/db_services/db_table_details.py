from datetime import datetime
from typing import List
from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.db_services.db_session import Base


from typing import Any, Dict, Optional
from sqlalchemy import BigInteger, DateTime, Integer, UniqueConstraint

from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import JSONB


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


class DocumentSource(Base):
    __tablename__ = "document_sources"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source_id: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )  # e.g. "company_handbook.md"
    source_path: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[str] = mapped_column(
        String(32), nullable=False
    )  # pdf/md/txt/docx/html/web
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA-256
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB, nullable=True
    )  # 'metadata' is reserved

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Optional but highly recommended: Establish a relationship to the chunks
    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Modernized to explicitly reference the unique source_id in DocumentSource
    source_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("document_sources.source_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[Any] = mapped_column(
        Vector(768), nullable=False
    )  # 768 for Gemini; switch to 384 for bge-small
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationship back to the source parent
    source: Mapped["DocumentSource"] = relationship(back_populates="chunks")

    __table_args__ = (
        UniqueConstraint("source_id", "chunk_index", name="uq_source_chunk_index"),
    )
