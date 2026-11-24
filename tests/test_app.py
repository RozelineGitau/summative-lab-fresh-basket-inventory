
import pytest
from app import app
from models import fruits


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    """Restore the original inventory before each test."""
    original = [
        {
            "id": 1,
            "name": "Mangoes",
            "category": "Tropical Fruits",
            "price": 100.00,
            "quantity": 50,
            "unit": "piece",
            "origin": "Kenya"
        },
        {
            "id": 2,
            "name": "Bananas",
            "category": "Tropical Fruits",
            "price": 120.00,
            "quantity": 80,
            "unit": "bunch",
            "origin": "Uganda"
        },
        {
            "id": 3,
            "name": "Apples",
            "category": "Temperate Fruits",
            "price": 50.00,
            "quantity": 100,
            "unit": "piece",
            "origin": "South Africa"
        },
        {
            "id": 4,
            "name": "Avocados",
            "category": "Tropical Fruits",
            "price": 30.00,
            "quantity": 8,
            "unit": "piece",
            "origin": "Kenya"
        },
        {
            "id": 5,
            "name": "Oranges",
            "category": "Citrus Fruits",
            "price": 25.00,
            "quantity": 0,
            "unit": "piece",
            "origin": "Kenya"
        }
    ]

    fruits.clear()
    fruits.extend(original)


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 5


def test_get_single_fruit(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Mangoes"


def test_get_missing_fruit(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404


def test_add_fruit(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Pineapples",
            "category": "Tropical Fruits",
            "price": 150,
            "quantity": 20,
            "unit": "piece",
            "origin": "Kenya"
        }
    )
    assert response.status_code == 201
    assert response.get_json()["name"] == "Pineapples"


def test_add_fruit_without_name(client):
    response = client.post(
        "/inventory",
        json={
            "category": "Tropical Fruits",
            "price": 150,
            "quantity": 20
        }
    )
    assert response.status_code == 400


def test_update_fruit(client):
    response = client.patch(
        "/inventory/1",
        json={"quantity": 65}
    )
    assert response.status_code == 200
    assert response.get_json()["quantity"] == 65


def test_update_missing_fruit(client):
    response = client.patch(
        "/inventory/999",
        json={"quantity": 10}
    )
    assert response.status_code == 404


def test_delete_fruit(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 204


def test_delete_missing_fruit(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


def test_low_stock(client):
    response = client.get("/inventory/low-stock")
    assert response.status_code == 200

    names = [fruit["name"] for fruit in response.get_json()]
    assert "Avocados" in names
    assert "Oranges" in names
