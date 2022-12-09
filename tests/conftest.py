import json
import os
import sys
from typing import Dict, Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_folder = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(root_folder)
from app.db.base import Base
from app.api.session import SessionLocal, get_db
from app.main import app
from app.api.api_v1.api import router

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg2://postgres:admin@localhost:5432/test_product"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def start_application():
    return app


SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def test_app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    app_test = start_application()
    yield app_test
    Base.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(test_app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(autouse=True)  #
def test_client(
    test_app: FastAPI, session: SessionTesting
) -> Generator[TestClient, Any, None]:  #
    def get_db_override():  #
        return session

    test_app.dependency_overrides[get_db] = get_db_override  #

    client = TestClient(test_app)  #
    yield client  #

    test_app.dependency_overrides.clear()  #
