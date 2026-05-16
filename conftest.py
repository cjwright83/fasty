import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from fasty.db import engine
from fasty.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    yield


@pytest.fixture(scope="module")
def client(setup_database):
    return TestClient(app)
