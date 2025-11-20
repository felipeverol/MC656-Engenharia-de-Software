import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.database import Base, get_db

# ----------------- SETUP BANCO TESTE -----------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/tests/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# ----------------- FIXTURES -----------------
@pytest.fixture
def register_user():
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "123456"
    }
    return client.post("/auth/register", json=payload)


@pytest.fixture
def token(register_user):
    login = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "123456"}
    )
    if login.status_code != 200:
        print("LOGIN FALHOU:", login.json())
    assert login.status_code == 200
    return login.json()["access_token"]
