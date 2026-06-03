from sqlalchemy import select, func
from sqlalchemy.orm import Session
from services.db_services.db_table_details import ChatSession, ChatMessage


def create_new_session(db: Session, title: str = "New Chat"):
    """Create a new chat session."""
    session_obj = ChatSession(title=title)
    db.add(session_obj)
    db.commit()
    db.refresh(session_obj)
    return session_obj


def get_all_sessions(db: Session):
    """Return all chat sessions ordered by latest updated."""
    # 2.0 Style: Explicitly select the model and execute via db.scalars
    stmt = select(ChatSession).order_by(ChatSession.updated_at.desc())
    return list(db.scalars(stmt).all())


def get_session_by_id(db: Session, session_id: int):
    """Fetch one chat session with its messages."""
    # 2.0 Style: db.get() is the cleanest way to look up a record by its primary key
    return db.get(ChatSession, session_id)


def add_message(db: Session, session_id: int, role: str, content: str):
    """Add a message to a chat session and update timestamp."""
    # We no longer pass created_at here.
    # The modern model's `server_default=func.now()` handles it automatically on the DB side.
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
    """Rename a chat session."""
    session_obj = db.get(ChatSession, session_id)
    if session_obj:
        session_obj.title = title

        # Note: If your modern model has `onupdate=func.now()`, changing the title
        # would automatically trigger an update. However, setting it explicitly
        # with func.now() ensures it updates even if nothing else changed.
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
