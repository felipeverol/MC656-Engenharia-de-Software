from fastapi.testclient import TestClient
# Esta linha vai procurar por um ficheiro chamado `main.py` dentro de uma pasta `app`
from app.main import app

client = TestClient(app)

def test_read_root_should_return_ok():
    """
    Testa se a rota raiz ("/") retorna o status code 200 (OK).
    Este é um teste "health check" para garantir que a API está a funcionar.
    """
    response = client.get("/")
    assert response.status_code == 200
