import json
from unittest.mock import MagicMock
import pytest
from pytest_mock import mocker
from app.core.config import settings
import httpx
from fastapi.responses import JSONResponse
from pytest_httpx import HTTPXMock
from app import crud
from app.main import app
from tests.conftest import SessionTesting
from tests.utils import (
    new_product_payload,
    create_product,
    get_product,
    delete_product,
    update_product,
    replace_do_something,
)


def test_can_call_endpoint(test_client):
    response = test_client.get(f"{settings.API_V1_STR}")
    assert response.status_code == 200


def test_create_product(test_client) -> None:

    test_request_payload = new_product_payload()
    response = create_product(test_client, test_request_payload)

    assert response.status_code == 201
    assert response.json()["message"] == "Product Created"
    data = response.json()
    # print(data)
    id = data["product_id"]
    get_response = get_product(test_client, id)

    assert get_response.status_code == 200
    get_data = get_response.json()

    assert get_data["name"] == test_request_payload["name"]


def test_read_with_error(test_client, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "app.api.api_v1.endpoints.product.create_product", replace_do_something
    )
    response = test_client.get("f{settings.API_V1_STR}/")
    print(response)
    assert response.status_code == 404
    assert response.json() == {"message": "Not Found"}


def test_create_product_invalid_json(test_client) -> None:
    response = test_client.post(
        f"{settings.API_V1_STR}/", content=json.dumps({"name": "something"})
    )
    assert response.status_code == 422


def test_read_product_incorrect_id(test_client) -> None:

    response = test_client.get(f"{settings.API_V1_STR}/999")
    assert response.status_code == 404
    assert response.json()["message"] == "product not found"


def test_read_all_products(test_client) -> None:
    response = test_client.get(f"{settings.API_V1_STR}/")
    # print(response)
    assert response.status_code == 200


def test_update_product(test_client) -> None:

    data = new_product_payload()

    create_response = create_product(test_client, data)
    product_id = create_response.json()["product_id"]

    new_payload = {
        "id": product_id,
        "name": "newtest",
        "brand": "abc123",
        "price": 20,
        "quantity": 0,
        "category": "category",
    }

    update_response = update_product(
        client=test_client, id=product_id, payload=new_payload
    )

    update_data = update_response.json()
    print(update_data)

    assert update_response.status_code == 200
    assert update_data["name"] == new_payload["name"]
    assert update_data["brand"] == new_payload["brand"]
    assert "id" in update_data

    get_response = get_product(client=test_client, id=product_id)

    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["name"] == new_payload["name"]


# def test_update_fail(client):


def test_deleteproduct(test_client, mocker) -> None:  # new
    data = new_product_payload()
    # Create a product.
    create_response = create_product(test_client, data)
    product_id = create_response.json()["product_id"]
    # Delete the product.
    delete_response = delete_product(test_client, product_id)
    assert delete_response.status_code == 200
    # Get the task,and check thats not found.
    get_response = get_product(test_client, product_id)

    assert get_response.status_code == 404


# def test_product_incorrect_id(test_client, mocker):
#     mocked=mocker.patch("app.api.api_v1.endpoints.product.get_product")
#     mocked.return_value=None

#     response =test_client.get(f"{settings.API_V1_STR}/999")
#     assert response.status_code == 404
#     assert response.json()["message"] == "product not found"

#     response =test_client.get(f"{settings.API_V1_STR}/0")
#     assert response.status_code == 404

# def test_delete_except(test_client):
#     with pytest.raises(Exception):
#         response=test_client.delete(f"{settings.API_V1_STR}/999")
#         assert response.status_code == 404


def test_update_except(test_client):
    with pytest.raises(Exception):
        response = test_client.put(f"{settings.API_V1_STR}/999")
        assert response.status_code == 404
