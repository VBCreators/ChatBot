from sqlalchemy.orm import Session, sessionmaker
from services.db_services.db_table_details import ChatSession
from sqlalchemy import func, create_engine, select, delete, update
from services.db_services.db_session import Base, engine
from config import DATABASE_URL

# def create_new_session(db_session: Session, title: str = "New Chat"):
#     # Create a new chat session


def insert_in_table(db_session: Session, table_obj, session_id, title):

    with db_session as session:
        table_obj.title = title
        # table_obj.session_id = session_id
        try:
            session.add(table_obj)
            session.commit()
            print("row inserted")
        except Exception as e:
            session.rollback()
            print(f"error is {e}")


def select_all_in_table(session: Session, table_class_name):
    table_output = session.scalars(select(table_class_name)).all()
    for row in table_output:
        print(
            f"Session id is: {row.session_id}  title is {row.title}   created on {row.created_at}   updated at {row.updated_at}"
        )


def delete_in_table(session: Session, table_class_name, delete_value):
    try:
        session.execute(
            delete(table_class_name).where(table_class_name.session_id == delete_value)
        )
        session.commit()

    except Exception as e:
        print(f"error occured while deleting. Error is {e}")
        session.rollback()


def lastupdate_in_table(session: Session, table_class_name, find_row_value):
    try:
        session.execute(
            update(table_class_name)
            .where(table_class_name.session_id == find_row_value)
            .values(updated_at=func.now())
        )
        session.commit()

    except Exception as e:
        print(f"error occured while updating. Error is {e}")
        session.rollback()


engine_obj = create_engine(DATABASE_URL, echo=True)
session_obj = sessionmaker(bind=engine_obj, autoflush=False, autocommit=False)

with session_obj() as session:
    table_obj = ChatSession()

    try:
        insert_in_table(session, table_obj, 14, "intro v6.0")
        # delete_in_table(session, ChatSession, 1)
        # lastupdate_in_table(session, ChatSession, 1)
        select_all_in_table(session, ChatSession)

    except Exception as e:
        print(f"error occured {e}")
        session.rollback()

    finally:
        session.close()
        print("program end")
