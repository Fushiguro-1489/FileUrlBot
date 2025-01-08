from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///bot.db"

class Base(DeclarativeBase):
	pass

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
	# === Create Tables ===
	Base.metadata.create_all(bind=engine)
