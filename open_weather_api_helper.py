import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city: str) -> dict:
    """
    Fetch current weather data for a city from OpenWeather API.
    
    Args:
        city: Name of the city

    Returns:
        Dictionary with weather information
    """
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch weather data"}
    
def parse_weather_data(data: dict) -> dict:
    """
    Parse weather data from OpenWeather API response.
    
    Args:
        data: Raw weather data from API

    Returns:
        Dictionary with parsed weather information
    """
    if "error" in data:
        return {"error": data["error"]}

    main = data.get("main", {})
    weather = data.get("weather", [{}])[0]

    return {
        "city": data.get("name"),
        "temperature": main.get("temp"),
        "condition": weather.get("description"),
        "humidity": main.get("humidity"),
        "wind_speed": data.get("wind", {}).get("speed")
    }

def get_weather(city: str) -> dict:
    """
    Get current weather for a city.

    Args:
        city: Name of the city

    Returns:
        Dictionary with weather information
    """
    data = fetch_weather(city)
    return parse_weather_data(data)

def get_forecast(city: str, days: int = 3) -> list:
    """
    Get weather forecast for a city.

    Args:
        city: Name of the city
        days: Number of days to forecast

    Returns:
        List of dictionaries with forecast information
    """
    logger.info(f"Getting {days}-day forecast for city: {city}")
    forecast = []
    for day in range(1, days + 1):
        data = fetch_weather(city)
        parsed = parse_weather_data(data)
        if "error" not in parsed:
            forecast.append(parsed)
    return forecast

