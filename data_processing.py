# data_processing.py
import requests
from datetime import datetime
from collections import defaultdict, Counter
from config import API_KEY, METROS, BASE_URL
import alerting
from db_manager import store_daily_summary

# Helper function to convert Kelvin to Celsius
def kelvin_to_celsius(temp_k):
    return temp_k - 273.15

# Dictionary to store daily weather data
daily_data = defaultdict(list)

def fetch_weather(city):
    params = {"q": city, "appid": API_KEY}
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    # Check if response contains valid data before processing
    if all(key in data for key in ["main", "weather", "dt"]):
        print(f"Fetched data for {city}: Temp - {data['main']['temp']}K, Condition - {data['weather'][0]['main']}")
        
        return {
            "city": city,
            "temp": kelvin_to_celsius(data["main"]["temp"]),
            "feels_like": kelvin_to_celsius(data["main"]["feels_like"]),
            "dt": datetime.fromtimestamp(data["dt"]),
            "condition": data["weather"][0]["main"]
        }
    
    print(f"Error fetching data for {city}: {data.get('message', 'Unknown error')}")
    return None

def aggregate_daily_data():
    today = datetime.now().date()
    temperatures, conditions = [], []

    # Gather all data for the current day
    for record in daily_data.get(today, []):
        temperatures.append(record["temp"])
        conditions.append(record["condition"])
    
    daily_summary = {
        "average_temp": sum(temperatures) / len(temperatures) if temperatures else 0,
        "max_temp": max(temperatures, default=0),
        "min_temp": min(temperatures, default=0),
        "dominant_condition": Counter(conditions).most_common(1)[0][0] if conditions else "N/A",
        "city": "All Cities",  # or set to a specific city if desired
        "date": today
    }

    print(f"Daily Weather Summary for {today}: {daily_summary}")
    return daily_summary

def process_and_store_data(alert_threshold):
    all_data = [fetch_weather(city) for city in METROS]
    all_data = [data for data in all_data if data is not None]  # Filter out None values

    for data in all_data:
        date_key = data["dt"].date()
        daily_data[date_key].append(data)
    
    daily_summary = aggregate_daily_data()
    
    # Store daily summary in the database and get status message
    status_message = store_daily_summary(daily_summary)

    # Check thresholds and trigger alerts if necessary
    alerts = alerting.check_thresholds(all_data, alert_threshold)
    
    # Return current data, daily summary, alerts, and status message
    return all_data, daily_summary, alerts, status_message
