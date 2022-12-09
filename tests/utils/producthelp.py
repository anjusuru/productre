import json
from app.core.config import settings
from fastapi.responses import JSONResponse


def new_product_payload():
    return {
        "name": "new",
        "brand": "abc1",
        "price": 0,
        "quantity": 0,
        "category": "category",
    }


def create_product(client, test_payload) -> JSONResponse:
    return client.post(f"{settings.API_V1_STR}/", content=json.dumps(test_payload))


def get_product(client, id) -> JSONResponse:
    return client.get(f"{settings.API_V1_STR}/{id}")


def update_product(client, id, payload) -> JSONResponse:
    return client.put(
        f"{settings.API_V1_STR}/{id}",
        content=json.dumps(payload),
    )


def delete_product(client, id) -> JSONResponse:
    return client.delete(f"{settings.API_V1_STR}/{id}")


def replace_do_something() -> None:
    raise Exception()
    return
