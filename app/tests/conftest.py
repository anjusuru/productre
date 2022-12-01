import json
import os
import sys
from typing import Dict, Generator

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
from app.api.session import SessionLocal
from main import app

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/test_product?connect_timeout=10"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(engine)


# @pytest.fixture(name="session")
# def session_fixture():
#     connection = engine.connect()
#     transaction = connection.begin()
#     session = SessionTesting(bind=connection)
#     yield session
#     session.close()
#     transaction.rollback()
#     connection.close()


# @pytest.fixture(autouse=True)  #
# def client_test(session: SessionTesting):  #
#     def get_db_override():  #
#         return session

#     app.dependency_overrides[get_db] = get_db_override  #

#     client = TestClient(app)  #
#     yield client  #
# app.dependency_overrides.clear()  #


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
