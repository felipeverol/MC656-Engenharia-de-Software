from app.tests.conftest import client


def test_add_to_cart(token):
    response = client.get("/cart/add/123456", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_get_cart(token):
    response = client.get("/cart", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_remove_from_cart(token):
    response = client.get("/cart/remove/123456", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]


def test_save_cart(token):
    response = client.post("/cart/save?cart_name=testcart", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
