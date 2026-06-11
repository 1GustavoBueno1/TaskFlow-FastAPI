from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


URL = "sqlite:///./Taskflow.db"
engine = create_engine(URL, connect_args={"check_same_thread": False})

Sessionlocal = sessionmaker(bind=engine, autoflush=False)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
Base = declarative_base()