from services.db_services.db_session import engine, Base
from services.db_services.db_table_details import (
    ChatSession,
    ChatMessage,
    Users,
)
# from sqlalchemy import text


Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
print(Base.metadata.tables.keys())


# def enable_pgvector():
#     # pgvector is a Postgres extension — must be enabled per-database.
#     with engine.begin() as conn:
#         conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))


# def create_all_tables():
#     Base.metadata.create_all(bind=engine)


# def create_vector_index():

#     # IVFFlat index: groups vectors into 100 clusters at build time.
#     # At query time, only the closest clusters are searched.
#     # ~10x faster than a full scan for >1K rows.

#     with engine.begin() as conn:
#         conn.execute(
#             text("""
#             CREATE INDEX IF NOT EXISTS idx_document_chunks_embedding
#             ON document_chunks
#             USING ivfflat (embedding vector_cosine_ops)
#             WITH (lists = 100);
#         """)
#         )


# if __name__ == "__main__":
#     enable_pgvector()  # MUST be first
#     create_all_tables()
#     create_vector_index()
#     print("RAG-ready.")
