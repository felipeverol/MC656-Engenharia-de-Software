from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_product():
    """
    Testa o endpoint de adicionar um produto ao carrinho.
    Verifica o status code, o JSON retornado e o estado do carrinho.
    """
    barcode_to_test = "3017624010701"
    response = client.get(f"/add/{barcode_to_test}")

    assert response.status_code == 200, f"Erro: Status Code foi {response.status_code}"

    data = response.json()
    assert "msg" in data
    assert "cart" in data
    assert isinstance(data["cart"], list)