import pytest  
from fastapi.testclient import TestClient
from app.main import app
from app.database.database import get_db
from app.database import schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# -------------------- AUTH TESTS --------------------

def test_register():
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_login():
    response = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    global token
    token = response.json()["access_token"]


def test_get_me():
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

# -------------------- CART TESTS --------------------

def test_add_to_cart():
    response = client.get("/cart/add/123456", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_get_cart():
    response = client.get("/cart", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_remove_from_cart():
    response = client.get("/cart/remove/123456", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_save_cart():
    response = client.post("/cart/save?cart_name=testcart", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
