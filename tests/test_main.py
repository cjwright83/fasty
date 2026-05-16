from fastapi.testclient import TestClient


def test_read_main_response_status_code_200(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_read_main_response_json(client: TestClient):
    response = client.get("/")
    assert response.json() == {"Hello": "World"}
