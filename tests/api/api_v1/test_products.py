import json
import pytest
from app.core.config import settings
import httpx
from pytest_httpx import HTTPXMock


def test_create_product(client) -> None:

    test_request_payload = {
        "name": "new",
        "brand": "abc1",
        "price": 0,
        "quantity": 0,
        "category": "category",
    }
    response = client.post(
        f"{settings.API_V1_STR}/",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Product Created"


def test_create_product_invalid_json(client):
    response = client.post(
        f"{settings.API_V1_STR}/", content=json.dumps({"name": "something"})
    )
    assert response.status_code == 422


def test_read_product_incorrect_id(client):

    response = client.get(f"{settings.API_V1_STR}/999")
    assert response.status_code == 404
    assert response.json()["message"] == "product not found"


def test_read_all_notes(client):
    response = client.get(f"{settings.API_V1_STR}/")
    assert response.status_code == 200


def test_update_product(client):
    data = {
        "name": "new",
        "brand": "asda",
        "price": 0,
        "quantity": 0,
        "category": "category",
    }
    client.post(
        f"{settings.API_V1_STR}/",
        content=json.dumps(data),
    )
    data["name"] = "test new title"
    response = client.put(
        f"{settings.API_V1_STR}/2",
        content=json.dumps(data),
    )
    assert response.status_code == 200


def test_deleteproduct(client):  # new
    data = {
        "name": "new",
        "brand": "ghi2",
        "price": 0,
        "quantity": 0,
        "category": "category",
    }
    client.post(
        f"{settings.API_V1_STR}/",
        content=json.dumps(data),
    )
    msg = client.delete(f"{settings.API_V1_STR}/3")
    response = client.get(f"{settings.API_V1_STR}/3")
    assert response.status_code == 404
