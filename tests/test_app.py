import pytest

from app import create_app


@pytest.fixture()
def client():
    application = create_app()
    application.config.update(TESTING=True)
    return application.test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {
        "status": "healthy",
        "application": "student-ml-api",
        "version": "1.0.0",
    }


def test_predict_success(client):
    response = client.post("/predict", json={"value": 10})
    assert response.status_code == 200
    assert response.get_json() == {"input": 10, "prediction": 20}


def test_predict_accepts_decimal(client):
    response = client.post("/predict", json={"value": 2.5})
    assert response.status_code == 200
    assert response.get_json() == {"input": 2.5, "prediction": 5.0}


def test_predict_rejects_missing_input(client):
    response = client.post("/predict", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required field: value"}


@pytest.mark.parametrize("value", ["ten", None, True])
def test_predict_rejects_invalid_input(client, value):
    response = client.post("/predict", json={"value": value})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Field 'value' must be a number"}


def test_predict_rejects_non_json(client):
    response = client.post("/predict", data="value=10")
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing required field: value"}
