from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker, session, declarative_base
from app.config import DATABASE_URL

engine: Engine = create_engine(DATABASE_URL, echo=False)
SessionLocal: session = sessionmaker(bind=engine)

Base = declarative_base()

with engine.connect() as connection:
    connection.execute(text("select 1"))
