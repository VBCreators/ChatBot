from sqlalchemy import select
from sqlalchemy.orm import Session
from services.db_services.db_table_details import ChatSession, ChatMessage


def create_new_session(db_session: Session, title: str = "New Chat"):
    # Create a new chat session

    table_obj = ChatSession(title=title)
    db_session.add(table_obj)
    db_session.commit()
    db_session.refresh(table_obj)
    return table_obj


def get_all_sessions(db_session: Session):
    # Return all chat sessions ordered by latest updated
    stmt = select(ChatSession).order_by(ChatSession.updated_at.desc())
    return list(db_session.scalars(stmt).all())
