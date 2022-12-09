from app.api.session import get_db
from fastapi import APIRouter, Depends
from app.schemas.product_schema import UpdateProduct, Product, CreateProduct
from app.crud import product_obj
from app import crud
from app.models.product import Product
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from pytest_mock import mocker
import unittest
from unittest.mock import patch
from app.api import session


def test_get_db(mocker, db: SessionLocal):

    print(SessionLocal)

    session_obj = get_db()
    mocked_session = mocker.patch("app.db.session.SessionLocal")

    print(mocked_session)
    # mocked_db = mocker.patch('app.api.session.get_db')

    # mocked_close=mocker.patch('app.api.session.close')

    name = "test"
    brand = "test8"
    price = 23
    quantity = 12
    category = "sddsf"

    p = Product(
        name=name, brand=brand, price=price, quantity=quantity, category=category
    )

    db.add(p)
    db.commit()

    # product_in = CreateProduct(name=name,brand=brand,price=price,quantity=quantity,category=category)

    # product_craeted=crud.product_obj.create(mocked_db,product_in)

    # print(product_craeted)

    session_obj = get_db()

    # mocked_session.assert_called()


# mocked_session.assert_called_once()
# class  TestSession(unittest.TestCase):

#      @patch('app.db.session.SessionLocal')
#      def test_get_db(self,mock_session_local):

#          mock_session_local.return_vale= None

#          self.assertM


#     session_obj = get_db()

#     session=SessionLocal()

#     assert session_obj

#     mock_now=mocker.patch("app.db.session.SessionLocal",return_value=None)


#     name="test"
#     brand= "test5"
#     price=  23
#     quantity= 12
#     category= "sddsf"

#     product_in = CreateProduct(name=name,brand=brand,price=price,quantity=quantity,category=category)

#     product_craeted=crud.product_obj.create(db=session, obj_in=product_in)
