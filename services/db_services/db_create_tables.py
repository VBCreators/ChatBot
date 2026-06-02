from services.db_services.db_session import engine, Base
import services.db_services.db_table_details

Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
