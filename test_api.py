from unittest.mock import patch

import pytest

from app.main import create_app

from app.services.weather_service import (
    CityNotFoundError,
    WeatherAPIError,
)


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_missing_city(client):
    response = client.get("/api/weather")

    assert response.status_code == 400

    assert (
        response.get_json()["error"]
        == "validation_error"
    )


def test_city_too_short(client):
    response = client.get("/api/weather?city=A")

    assert response.status_code == 400


@patch("app.routes.get_weather")
def test_weather_success(mock_weather, client):
    mock_weather.return_value = {
        "location": {
            "city": "Agra",
            "country": "India",
            "latitude": 27.1767,
            "longitude": 78.0081,
        },
        "weather": {
            "temperature_c": 30.0,
            "feels_like_c": 32.0,
            "humidity_percent": 55,
            "wind_speed_kmh": 10.5,
            "weather_code": 1,
        },
        "timezone": "Asia/Kolkata",
    }

    response = client.get("/api/weather?city=Agra")

    assert response.status_code == 200
    assert response.get_json()["location"]["city"] == "Agra"


@patch("app.routes.get_weather")
def test_city_not_found(mock_weather, client):
    mock_weather.side_effect = CityNotFoundError(
        "No location was found for 'UnknownCity'."
    )

    response = client.get(
        "/api/weather?city=UnknownCity"
    )

    assert response.status_code == 404

    assert (
        response.get_json()["error"]
        == "city_not_found"
    )


@patch("app.routes.get_weather")
def test_weather_service_error(mock_weather, client):
    mock_weather.side_effect = WeatherAPIError(
        "Could not reach the weather service."
    )

    response = client.get("/api/weather?city=Agra")

    assert response.status_code == 502

    assert (
        response.get_json()["error"]
        == "weather_api_error"
    )


@patch("app.routes.get_weather")
def test_unexpected_error(mock_weather, client):
    mock_weather.side_effect = RuntimeError("unexpected")

    response = client.get("/api/weather?city=Agra")

    assert response.status_code == 500

    assert (
        response.get_json()["error"]
        == "internal_server_error"
    )