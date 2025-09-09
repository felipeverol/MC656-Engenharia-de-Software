from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_add_product_found():
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

def test_add_product_not_found():
    """
    Testa o endpoint de adicionar um produto ao carrinho com um código de barras inválido.
    Verifica se o status code é 404 e a mensagem de erro correta.
    """
    invalid_barcode = "0000000000000"
    response = client.get(f"/add/{invalid_barcode}")

    assert response.status_code == 404, f"Erro: Status Code foi {response.status_code}"

    data = response.json()
    assert data["detail"] == "Product not found"