from app.tests.conftest import client


def test_register(register_user):
    assert register_user.status_code == 200


def test_login(token):
    assert token is not None


def test_get_me(token):
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200