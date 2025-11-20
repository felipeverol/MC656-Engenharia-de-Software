from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import database

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/database/cart.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Dependência do banco ---
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()