# server.py - Simple Weather MCP Server
from fastmcp import FastMCP
import random
import logging
import open_weather_api_helper as weather_helper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info(f"Getting weather for city: {city}")

    weather_data = weather_helper.get_weather(city)
    
    logger.info(f"Weather data for {city}: {weather_data['condition']}, {weather_data['temperature']}°C")
    return weather_data

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
    logger.info(f"Getting {days}-day forecast for city: {city}")
    forecast = weather_helper.get_forecast(city, days)
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
    logger.info(f"Accessing weather resource for city: {city}")
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
    logger.info(f"Generating weather analysis prompt for city: {city}")
    return f"Analyze the current weather conditions in {city} and provide " \
           f"recommendations for outdoor activities."

# CRITICAL: Run the server
if __name__ == "__main__":
    logger.info("Starting Weather MCP Server with OpenWeatherAPI...")
    mcp.run()
