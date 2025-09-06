# test_main.py
from fastapi.testclient import TestClient

# Importamos o 'app' do arquivo backend/main.py
from backend.main import app

# Criamos um cliente de teste para fazer as requisições
client = TestClient(app)

def test_add_product_to_cart():
    """
    Testa o endpoint de adicionar um produto (mockado) ao carrinho.
    Verifica o status code, o JSON retornado e o estado do carrinho.
    """
    client.delete("/cart") # Limpa o carrinho usando o endpoint

    barcode_to_test = "7891234567890" # Um código de barras de exemplo
    response = client.post(f"/add_product/{barcode_to_test}")

    assert response.status_code == 200, f"Erro: Status Code foi {response.status_code}"

    data = response.json()
    assert "product" in data
    assert "quantity" in data
    assert data["product"]["name"] == "Produto Exemplo"
    assert data["product"]["barcode"] == barcode_to_test
    assert data["quantity"] == 1

def test_list_cart():
    """
    Testa o endpoint que lista os itens do carrinho.
    """
    client.delete("/cart") # Garante um carrinho limpo

    client.post("/add_product/7891234567890")

    response = client.get("/cart")

    assert response.status_code == 200
    cart_data = response.json()
    assert isinstance(cart_data, list)
    assert len(cart_data) == 1
    assert cart_data[0]["quantity"] == 1
    assert cart_data[0]["product"]["name"] == "Produto Exemplo"

def test_delete_cart():
    """
    Testa se o endpoint de limpar o carrinho funciona.
    """
    client.post("/add_product/7891234567890")

    response = client.delete("/cart")
    assert response.status_code == 200
    assert response.json() == {"message": "Carrinho esvaziado com sucesso."}

    get_response = client.get("/cart")
    assert get_response.status_code == 200
    assert get_response.json() == []