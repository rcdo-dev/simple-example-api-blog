from sqlmodel import Session, SQLModel, create_engine

from core.config import settings

sqlite_url = settings.DATABASE_URL

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
