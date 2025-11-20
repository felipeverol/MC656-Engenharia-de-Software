from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app 
from app.utils.product import Product
from app.routers.cart_router import get_current_user_id, user_carts
from app.database.database import get_db
from app.database.models import Base 

# -----------------------------------------------------------
# Configuração do DB em Memória para Testes
# -----------------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def override_auth_no_check():
    return 999
app.dependency_overrides[get_current_user_id] = override_auth_no_check
# -----------------------------------------------------------

client = TestClient(app)
TEST_USER_EMAIL = "ci_test@example.com"
TEST_USER_PASSWORD = "TestPassword123"

# --- Fixtures de Usuário e Token ---

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Cria as tabelas no DB em memória antes de todos os testes."""
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture(scope="module")
def test_user_token():
    """Registra um usuário de teste, faz login e retorna o token de acesso."""
    # 1. Registro
    user_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "is_active": True
    }
    client.post("/auth/register", json=user_data)

    # 2. Login para obter o token
    login_data = {
        "username": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json().get("access_token")
        
    auth_header = {"Authorization": f"Bearer {token}"}

    yield auth_header


@pytest.fixture(autouse=True)
def clean_cart_state():
    """Garante que o estado global do carrinho esteja limpo antes de cada teste."""
    user_carts.clear()
    yield

# --- Testes de Autenticação ---

def test_auth_register_and_login():
    """Testa se o registro e login funcionam isoladamente."""
    response = client.get("/auth/me", headers={"Authorization": "Bearer BAD_TOKEN"})
    assert response.status_code == 401
    
    user_data = {"email": "ci_test2@example.com", "password": "TestPassword123", "is_active": True}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

# --- Testes de Carrinho ---

def test_get_empty_cart(test_user_token):
    """Testa se o carrinho retorna 404 quando vazio."""
    response = client.get("/cart", headers=test_user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cart not found"


@patch('app.utils.product_service.ProductService.fetch_product')
def test_get_cart_with_items(mock_fetch_product, test_user_token):
    """Testa o fluxo completo: Adicionar item -> Verificar no carrinho."""
    mock_fetch_product.return_value = Product(
        code="737628064502",
        name="Coca-Cola",
        nutriments={"energy-kcal_100g": 42}
    )
    
    client.get("/cart/add/737628064502", headers=test_user_token) 

    response = client.get("/cart", headers=test_user_token)
    assert response.status_code == 200
    data = response.json()
    assert data["cart"]["total_items"] == 1
    assert data["cart"]["products"][0]["name"] == "Coca-Cola"


@patch('app.utils.product_service.ProductService.fetch_product')
def test_remove_item_successfully(mock_fetch_product, test_user_token):
    """Testa a remoção de um item existente."""
    mock_fetch_product.return_value = Product(
        code="737628064502",
        name="Coca-Cola",
        nutriments={"energy-kcal_100g": 42}
    )

    client.get("/cart/add/737628064502", headers=test_user_token)
    response = client.get("/cart/remove/737628064502", headers=test_user_token)
    assert response.status_code == 200

    final_cart_response = client.get("/cart", headers=test_user_token)
    assert final_cart_response.status_code == 404


def test_remove_item_not_found(test_user_token):
    """Testa a remoção de um item inexistente."""
    response = client.get("/cart/remove/non_existent_barcode", headers=test_user_token)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found in cart"

@patch('app.utils.product_service.ProductService.fetch_product')
def test_add_product_found(mock_fetch_product, test_user_token):
    """Testa a adição de um produto válido."""
    mock_fetch_product.return_value = Product(
        code="3017624010701",
        name="Test Product",
        nutriments={"energy-kcal_100g": 50}
    )

    barcode_to_test = "3017624010701"
    response = client.get(f"/cart/add/{barcode_to_test}", headers=test_user_token)
    assert response.status_code == 200

    data = response.json()
    assert data["cart"] == ["Test Product"]


def test_add_product_not_found(test_user_token):
    """Testa a adição quando o serviço externo não encontra o produto."""
    with patch('app.utils.product_service.ProductService.fetch_product', return_value=None):
        invalid_barcode = "93017624010701"
        response = client.get(f"/cart/add/{invalid_barcode}", headers=test_user_token)

        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
        
# --- Teste da Rota de Salvamento ---

@patch('app.database.crud.create_user_cart')
@patch('app.utils.product_service.ProductService.fetch_product')
def test_save_cart_successfully(mock_fetch_product, mock_crud_create, test_user_token):
    """Testa o salvamento do carrinho e a limpeza posterior."""
    # 1. Setup do Mock para o produto
    mock_fetch_product.return_value = Product(
        code="737628064502",
        name="Coca-Cola",
        nutriments={"energy-kcal_100g": 42}
    )
    # 2. Pré-condição: Adicionar item
    client.get("/cart/add/737628064502", headers=test_user_token)

    # 3. Setup do Mock para a função de salvamento no DB
    mock_crud_create.return_value = {"id": 1, "name": "Compras de Julho"}
    
    # 4. Ação: Salvar o carrinho
    response = client.post("/cart/save?cart_name=Compras de Julho", headers=test_user_token)
    
    assert response.status_code == 200
    assert response.json()["msg"] == "Cart saved!"
    
    # 5. Verificação: Carrinho deve estar vazio após salvar
    final_cart_response = client.get("/cart", headers=test_user_token)
    assert final_cart_response.status_code == 404