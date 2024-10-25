# config.py
import os
API_KEY = os.getenv("API_KEY") 
METROS = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Abc@1234567890",
    "database": "weather_data"
}

INTERVAL = 300  # Fetch interval in seconds (e.g., every 5 minutes)
ALERT_THRESHOLD = 35  # Example threshold for temperature alerts in Celsius

# Specific weather conditions to monitor
SPECIFIC_CONDITIONS = ["Rain", "Snow", "Thunderstorm"]  # Add any other conditions you want to monitor