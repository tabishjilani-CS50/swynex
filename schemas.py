def validate_city(city):
    """Validate and normalize the city name."""

    if city is None:
        raise ValueError("City is required.")

    city = city.strip()

    if not city:
        raise ValueError("City is required.")

    if len(city) < 2:
        raise ValueError(
            "City must contain at least 2 characters."
        )

    if len(city) > 100:
        raise ValueError(
            "City must contain at most 100 characters."
        )

    return city