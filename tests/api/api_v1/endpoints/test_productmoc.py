from pytest_mock import mocker
import json
from app.crud.base import CRUDBase
from app.core.config import settings
from app.api.api_v1.endpoints.product import update_product, delete_item


def test_update_fail(mocker, test_client):

    # client = TestClient(app)
    id = 0
    mocked = mocker.patch("app.crud.base.CRUDBase.get")
    mocked.return_value = None

    new_payload = {
        "id": id,
        "name": "newtest",
        "brand": "abc123",
        "price": 20,
        "quantity": 0,
        "category": "category",
    }

    response = test_client.put(
        f"{settings.API_V1_STR}/{id}",
        content=json.dumps(new_payload),
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Product not found"


def test_delete_fail(mocker, test_client):

    id = 0
    mocked = mocker.patch("app.crud.base.CRUDBase.get")
    mocked.return_value = None

    response = test_client.delete(
        f"{settings.API_V1_STR}/{id}",
    )

    assert response.status_code == 404
    assert response.json()["message"] == "Product not found"
