import os
import dotenv
dotenv.load_dotenv()
os.environ.setdefault("JWT_SECRET", "chave-teste")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from app.models.models.database import Base, get_db


URL_TESTE = "sqlite:///:memory:"
engine_teste = create_engine(URL_TESTE, connect_args={"check_same_thread": False}, poolclass = StaticPool)
sessionteste = sessionmaker(bind = engine_teste)

def get_db_teste():
    db = sessionteste()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = get_db_teste

@pytest.fixture
def cliente():
    Base.metadata.create_all(bind = engine_teste)
    yield TestClient(app)
    Base.metadata.drop_all(bind = engine_teste)