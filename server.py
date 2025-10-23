# server.py - Simple Weather MCP Server
from fastmcp import FastMCP
import random

# Initialize MCP server with a descriptive name
mcp = FastMCP("Weather Service")

# Tool 1: Get current weather for a city
@mcp.tool()
def get_weather(city: str) -> dict:
    """
    Get current weather information for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Dictionary with weather information
    """
    # Simulate weather data (in production, call a real weather API)
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Stormy"]
    
    return {
        "city": city,
        "temperature": random.randint(10, 35),
        "condition": random.choice(conditions),
        "humidity": random.randint(30, 90),
        "wind_speed": random.randint(5, 25)
    }

# Tool 2: Get weather forecast
@mcp.tool()
def get_forecast(city: str, days: int = 3) -> list:
    """
    Get weather forecast for the next few days.
    
    Args:
        city: Name of the city
        days: Number of days to forecast (default: 3)
        
    Returns:
        List of daily forecasts
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
    forecast = []
    
    for day in range(1, days + 1):
        forecast.append({
            "day": day,
            "city": city,
            "temperature": random.randint(10, 35),
            "condition": random.choice(conditions)
        })
    
    return forecast

# Resource: City weather data
@mcp.resource("weather://{city}")
def get_city_weather_resource(city: str) -> str:
    """
    Resource providing weather context for a city.
    
    Args:
        city: Name of the city
        
    Returns:
        Formatted weather information
    """
    weather = get_weather(city)
    return f"Current weather in {weather['city']}: {weather['condition']}, " \
           f"{weather['temperature']}°C, Humidity: {weather['humidity']}%, " \
           f"Wind: {weather['wind_speed']} km/h"

# Prompt: Weather analysis template
@mcp.prompt()
def analyze_weather(city: str) -> str:
    """
    Provide a prompt template for weather analysis.
    
    Args:
        city: Name of the city
        
    Returns:
        Prompt for LLM to analyze weather
    """
    return f"Analyze the current weather conditions in {city} and provide " \
           f"recommendations for outdoor activities."

# CRITICAL: Run the server
if __name__ == "__main__":
    mcp.run()
