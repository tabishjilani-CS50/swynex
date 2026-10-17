# Weather Intelligence API — Flask

A Python backend project built with Flask that consumes
public weather APIs and returns current weather as JSON.

## Features

- Flask REST API
- Public Open-Meteo API integration
- City name validation
- Network timeout handling
- Error handling
- JSON responses
- Health-check endpoint
- Automated tests with pytest
- No API key required

## Endpoints

### Health check

GET /api/health

### Current weather

GET /api/weather?city=Agra

## Installation

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1