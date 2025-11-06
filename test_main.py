from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app

client = TestClient(app)

def test_get_empty_cart():
    response = client.get("/cart")
    assert response.status_code == 200
    expected_data = {
        "cart": {
            "total_items": 0,
            "products": []
        }
    }
    assert response.json() == expected_data

@patch('app.utils.product_service.ProductService.fetch_product')
def test_get_cart_with_items(mock_fetch_product):
    mock_fetch_product.return_value = Mock(
        code="737628064502",
        name="Coca-Cola",
        nutriments={"energy-kcal_100g": 42},
        to_dict={
            "code": "737628064502",
            "name": "Coca-Cola",
            "nutriments": {"energy-kcal_100g": 42}
        }
    )

    add_response = client.get("/add/737628064502")
    assert add_response.status_code == 200

    response = client.get("/cart")
    assert response.status_code == 200
    data = response.json()
    assert data["cart"]["total_items"] == 1
    assert data["cart"]["products"][0]["name"] == "Coca-Cola"
    assert data["cart"]["products"][0]["code"] == "737628064502"

@patch('app.utils.product_service.ProductService.fetch_product')
def test_remove_item_successfully(mock_fetch_product):
    mock_fetch_product.return_value = Mock(
        code="737628064502",
        name="Coca-Cola",
        nutriments={"energy-kcal_100g": 42},
        to_dict={
            "code": "737628064502",
            "name": "Coca-Cola",
            "nutriments": {"energy-kcal_100g": 42}
        }
    )

    client.get("/delete/cart")
    client.get("/add/737628064502")

    response = client.get("/remove/737628064502")
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "737628064502 removed!"
    assert data["cart"] == []

    final_cart_response = client.get("/cart")
    assert final_cart_response.json()["cart"]["total_items"] == 0

def test_remove_item_not_found():
    client.get("/delete/cart")
    response = client.get("/remove/non_existent_barcode")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found in cart"

@patch('app.utils.product_service.ProductService.fetch_product')
def test_add_product_found(mock_fetch_product):
    mock_fetch_product.return_value = Mock(
        code="3017624010701",
        name="Test Product",
        nutriments={"energy-kcal_100g": 50},
        to_dict={
            "code": "3017624010701",
            "name": "Test Product",
            "nutriments": {"energy-kcal_100g": 50}
        }
    )

    barcode_to_test = "3017624010701"
    response = client.get(f"/add/{barcode_to_test}")
    assert response.status_code == 200

    data = response.json()
    assert "msg" in data
    assert "cart" in data
    assert isinstance(data["cart"], list)

def test_add_product_not_found():
    invalid_barcode = "93017624010701"
    response = client.get(f"/add/{invalid_barcode}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"