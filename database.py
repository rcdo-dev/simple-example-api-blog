from sqlmodel import create_engine, SQLModel, Session

DATABASE_FILE = "blog.db"
sqlite_url = f"sqlite:///{DATABASE_FILE}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session