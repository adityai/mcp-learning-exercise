# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the OpenWeather API.

## Setup

### Environment Variables

Set your OpenWeather API key:
```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

Or create a `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
```

### Docker Usage

Run in detached mode:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop container:
```bash
docker-compose down
```

## Features

- Get current weather for any city
- Get weather forecast
- Weather data resources
- Weather analysis prompts