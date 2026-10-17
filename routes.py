from flask import Blueprint, jsonify, request

from app.schemas import validate_city

from app.services.weather_service import (
    CityNotFoundError,
    WeatherAPIError,
    get_weather,
)


weather_bp = Blueprint("weather", __name__)


@weather_bp.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "weather-intelligence-api"
    }), 200


@weather_bp.get("/weather")
def weather():
    city = request.args.get("city", "")

    try:
        city = validate_city(city)

        data = get_weather(city)

        return jsonify(data), 200

    except ValueError as exc:
        return jsonify({
            "error": "validation_error",
            "message": str(exc)
        }), 400

    except CityNotFoundError as exc:
        return jsonify({
            "error": "city_not_found",
            "message": str(exc)
        }), 404

    except WeatherAPIError as exc:
        return jsonify({
            "error": "weather_api_error",
            "message": str(exc)
        }), 502

    except Exception:
        return jsonify({
            "error": "internal_server_error",
            "message": "An unexpected error occurred."
        }), 500