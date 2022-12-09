from sqlalchemy.orm import Session

import app
from app.crud.base import CRUDBase
from app.models import Product
from sqlalchemy.orm import Session

from app.crud import base
from app.schemas.product_schema import UpdateProduct, Product, CreateProduct
from tests.utils.producthelp import new_product_payload
from pytest_mock import mocker
from app.crud import product_obj
from app import crud


def test_update_with_dicti(session, test_client) -> None:

    name = "test"
    brand = "test3"
    price = 23
    quantity = 12
    category = "sddsf"

    product_in = CreateProduct(
        name=name, brand=brand, price=price, quantity=quantity, category=category
    )

    product_craeted = crud.product_obj.create(db=session, obj_in=product_in)

    payload = {
        "name": "test",
        "brand": "test3",
        "price": 123,
        "quantity": 12,
        "category": "sddsf",
    }

    # product_update=UpdateProduct(name=name,brand=brand,price=price2,quantity=quantity,category=category)

    product_updated = crud.product_obj.update(
        db=session, db_obj=product_craeted, obj_in=payload
    )

    print(product_updated)

    assert product_craeted.id == product_updated.id

    assert product_updated.price == payload["price"]
