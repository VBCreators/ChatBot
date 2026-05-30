from sqlalchemy import create_engine, MetaData, table, column, integer, string, text

engine = create_engine(
    "postgresql://postgres:workforfire@localhost:5432/chatbot_database", echo=True
)

conn = engine.connect()

# conn.execute(text("CREATE TABLE IF NOT EXISTS people (name varchar, age int);"))

meta = MetaData()

teachers = table(
    "teachers",
    meta,
    column("id", integer, primary_key=True),
    column("name", string),
    column("age", integer, nullable=False),
)


meta.create_all(engine)

conn.commit()

print("last line")
