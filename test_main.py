from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)

def test_get_empty_cart():
    """
    Testa se a rota `/cart` se comporta corretamente quando o carrinho está vazio.

    Este teste executa os seguintes passos:
    1. Faz uma requisição GET para a rota `/cart`.
    2. Verifica se o código de status da resposta é 200 (OK).
    3. Verifica se o corpo da resposta JSON corresponde à estrutura esperada para um
       carrinho vazio, contendo 0 itens no total e uma lista de produtos vazia.
    """
    # Inicialmente o carrinho inicia vazio
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
    2. Preparação: O carrinho começa esvaziado e, em seguida, a rota `/add` é
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

    # 2. Setup: Carrinho é iniciado vazio e depois adiciona um produto
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
    invalid_barcode = "93017624010701"
    response = client.get(f"/add/{invalid_barcode}")

    assert response.status_code == 404, f"Erro: Status Code foi {response.status_code}"

    data = response.json()
    assert data["detail"] == "Product not found"