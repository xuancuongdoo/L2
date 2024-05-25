import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_travel_recommendations_success():
    response = client.get("/api/v1/recommendations?country=thailand&season=summer")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Success"
    assert data["data"]["country"] == "Thailand"
    assert data["data"]["season"] == "summer"
    assert isinstance(data["data"]["recommendations"], list)


def test_get_travel_recommendations_invalid_country():
    response = client.get("/api/v1/recommendations?country=thailandd&season=summer")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Failed"
    assert "InvalidCountryError" in data["data"]["error"]["type"]
    assert (
        "The provided country name 'thailandd' is not valid."
        in data["data"]["error"]["message"]
    )


def test_get_travel_recommendations_invalid_season():
    response = client.get("/api/v1/recommendations?country=thailand&season=autumn")
    assert response.status_code == 422  # Unprocessable Entity due to validation error
    data = response.json()
    assert (
        data["detail"][0]["msg"]
        == "String should match pattern '^(spring|summer|fall|winter)$'"
    )
