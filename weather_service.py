import requests

GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

WEATHER_URL = (
    "https://api.open-meteo.com/v1/forecast"
)

TIMEOUT = 8


class CityNotFoundError(Exception):
    pass


class WeatherAPIError(Exception):
    pass


def get_coordinates(city):
    """Find a city's latitude and longitude."""

    try:
        response = requests.get(
            GEOCODING_URL,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=TIMEOUT,
        )

        response.raise_for_status()
        payload = response.json()

    except (requests.RequestException, ValueError) as exc:
        raise WeatherAPIError(
            "Could not reach the location service."
        ) from exc

    results = payload.get("results") or []

    if not results:
        raise CityNotFoundError(
            f"No location was found for '{city}'."
        )

    location = results[0]

    try:
        return {
            "name": location["name"],
            "country": location.get("country"),
            "latitude": float(location["latitude"]),
            "longitude": float(location["longitude"]),
        }

    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherAPIError(
            "The location service returned invalid data."
        ) from exc


def get_weather(city):
    """Fetch the current weather for a city."""

    location = get_coordinates(city)

    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "wind_speed_10m,"
                    "weather_code"
                ),
                "timezone": "auto",
            },
            timeout=TIMEOUT,
        )

        response.raise_for_status()
        payload = response.json()

    except (requests.RequestException, ValueError) as exc:
        raise WeatherAPIError(
            "Could not reach the weather service."
        ) from exc

    current = payload.get("current")

    if not isinstance(current, dict):
        raise WeatherAPIError(
            "The weather service returned invalid data."
        )

    required_fields = [
        "temperature_2m",
        "relative_humidity_2m",
        "apparent_temperature",
        "wind_speed_10m",
        "weather_code",
    ]

    if any(field not in current for field in required_fields):
        raise WeatherAPIError(
            "The weather response is missing required fields."
        )

    return {
        "location": {
            "city": location["name"],
            "country": location["country"],
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        },
        "weather": {
            "temperature_c": current["temperature_2m"],
            "feels_like_c": current["apparent_temperature"],
            "humidity_percent": current[
                "relative_humidity_2m"
            ],
            "wind_speed_kmh": current["wind_speed_10m"],
            "weather_code": current["weather_code"],
        },
        "timezone": payload.get("timezone"),
    }