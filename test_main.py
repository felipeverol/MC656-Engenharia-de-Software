from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
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

def test_get_empty_cart():
    """
    Testa se a rota `/cart` se comporta corretamente quando o carrinho está vazio.

    Este teste executa os seguintes passos:
    1. Garante um estado limpo chamando a rota `/delete/cart` para esvaziar o carrinho.
    2. Faz uma requisição GET para a rota `/cart`.
    3. Verifica se o código de status da resposta é 200 (OK).
    4. Verifica se o corpo da resposta JSON corresponde à estrutura esperada para um
       carrinho vazio, contendo 0 itens no total e uma lista de produtos vazia.
    """
    # Primeiro, garante que o carrinho esteja vazio chamando a rota de exclusão
    client.get("/delete/cart")

    # Agora, solicita o carrinho
    response = client.get("/cart")
    
    # Afirma que a requisição foi bem-sucedida (status 200)
    assert response.status_code == 200 
    
    # O resultado deve mostrar 0 itens
    expected_data = {
        "cart": {
            "total_items": 0,
            "products": []
        }
    }
    assert response.json() == expected_data

# Usa o patch para substituir `requests.get` por um objeto "mock" (simulado)
@patch('requests.get')
def test_get_cart_with_items(mock_get):
    """
    Testa se a rota `/cart` retorna corretamente os itens após um produto ser adicionado.

    Este teste utiliza um "mock" para simular a chamada à API externa, evitando uma
    requisição de rede real e garantindo que o teste seja rápido e independente.

    Passos do teste:
    1. Configuração do Mock: O decorador `@patch` intercepta `requests.get`.
       Configuramos o `mock_get` para retornar uma resposta falsa bem-sucedida
       (status 200) com dados de um produto ("Coca-Cola").
    2. Preparação: O carrinho é esvaziado e, em seguida, a rota `/add` é
       chamada. A lógica interna dessa rota tentará usar `requests.get`, que será
       interceptada pelo nosso mock.
    3. Ação: A rota `/cart` é chamada para obter o estado atual do carrinho.
    4. Verificação: O teste verifica se a resposta tem status 200 e se
       o conteúdo JSON reflete corretamente a adição do produto, com o total de itens
       igual a 1 e os dados do produto correspondendo ao que foi simulado.
    """
    # 1. Configura o Mock para simular uma chamada de API bem-sucedida
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "product": {
            "code": "737628064502",
            "product_name": "Coca-Cola",
            "nutriscore_data": {"grade": "e"},
            "nutriments": {"energy-kcal_100g": 42}
        }
    }
    mock_get.return_value = mock_response

    # 2. Setup: Garante que o carrinho esteja vazio e depois adiciona um produto
    client.get("/delete/cart")
    add_response = client.get("/add/737628064502")
    assert add_response.status_code == 200

    # 3. Ação: Chama a rota que estamos testando
    response = client.get("/cart")

    # 4. Assert: Verifica o status e o conteúdo da resposta
    assert response.status_code == 200
    data = response.json()
    assert data["cart"]["total_items"] == 1
    assert data["cart"]["products"][0]["name"] == "Coca-Cola"
    assert data["cart"]["products"][0]["code"] == "737628064502"
    
@patch('app.cart.requests.get')
def test_remove_item_successfully(mock_get):
    """
    Testa a remoção bem-sucedida de um item que existe no carrinho.

    Este teste executa os seguintes passos:
    1. Configuração do Mock: Simula a API externa para que possamos adicionar um 
       produto ao carrinho sem fazer uma chamada de rede real.
    2. Preparação: O carrinho é limpo e um produto ("Coca-Cola") é adicionado
       para garantir que o carrinho não esteja vazio.
    3. Ação: A rota `/remove/{barcode}` é chamada com o código de barras
       do produto que acabamos de adicionar.
    4. Verificação: O teste confirma que:
       - O status da resposta é 200 (OK).
       - A mensagem de sucesso é retornada no JSON.
       - O carrinho, como parte da resposta, está agora vazio.
       - Uma chamada subsequente a `/cart` confirma que o número total de itens é 0.
    """
    # 1. Configura o Mock para simular a adição de um produto
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "product": { "code": "737628064502", "product_name": "Coca-Cola" }
    }
    mock_get.return_value = mock_response

    # 2. Setup: Adiciona um item ao carrinho
    client.get("/delete/cart")
    client.get("/add/737628064502")

    # 3. Ação: Remove o item
    response = client.get("/remove/737628064502")

    # 4. Assert: Verifica se a remoção foi bem-sucedida
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "737628064502 removed!"
    assert data["cart"] == [] # A lista de nomes de produtos no carrinho deve estar vazia

    # Verifica o estado final do carrinho para ter certeza
    final_cart_response = client.get("/cart")
    assert final_cart_response.json()["cart"]["total_items"] == 0
    
def test_remove_item_not_found():
    """
    Testa a resposta de erro ao tentar remover um item que não está no carrinho.

    Este teste executa os seguintes passos:
    1. Preparação: Garante que o carrinho esteja vazio chamando `/delete/cart`.
    2. Ação: Chama a rota `/remove/{barcode}` com um código de barras
       que certamente não existe no carrinho.
    3. Verificação: O teste confirma que a aplicação respondeu corretamente
       com um código de status 404 (Not Found) e que a mensagem de detalhe do erro
       é a esperada ("Product not found in cart").
    """
    # 1. Setup: Garante que o carrinho esteja vazio
    client.get("/delete/cart")

    # 2. Ação: Tenta remover um item inexistente
    response = client.get("/remove/non_existent_barcode")

    # 3. Assert: Verifica se o erro 404 foi retornado
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found in cart"