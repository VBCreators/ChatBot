from sqlalchemy import select, func
from sqlalchemy.orm import Session
from services.db_services.db_table_details import ChatSession, ChatMessage


def create_new_session(db: Session, title: str = "New Chat"):
    # Create a new chat session.
    session_obj = ChatSession(title=title)
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj


def get_all_sessions(db: Session):
    # Return all chat sessions ordered by latest updated.
    stmt = select(ChatSession).order_by(ChatSession.updated_at.desc())
    return list(db.scalars(stmt).all())


def get_session_by_id(db: Session, session_id: int):
    # Fetch one chat session with its messages."""
    return db.get(ChatSession, session_id)


def add_message(db: Session, session_id: int, role: str, content: str):
    # Add a message to a chat Message Table and update timestamp.

    message = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(message)

    # Update session timestamp using func.now() instead of Python's utcnow()
    session_obj = db.get(ChatSession, session_id)
    if session_obj:
        session_obj.updated_at = func.now()

    db.commit()
    db.refresh(message)
    return message


def update_session_title(db: Session, session_id: int, title: str):
    # Rename a chat session.
    session_obj = db.get(ChatSession, session_id)
    if session_obj:
        session_obj.title = title
        session_obj.updated_at = func.now()

        db.commit()
        db.refresh(session_obj)
    return session_obj


def delete_session(db: Session, session_id: int):
    """Delete a chat session and all its messages."""
    session_obj = db.get(ChatSession, session_id)
    if session_obj:
        db.delete(session_obj)
        db.commit()
        return True
    return False
