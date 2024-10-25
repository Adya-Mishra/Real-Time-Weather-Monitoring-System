#main.py
import schedule
import time
from data_processing import process_and_store_data

def run_system():
    print("Fetching weather data...")
    process_and_store_data()  # This will fetch data and store or print as configured

# Fetch data immediately at the start
print("Weather Monitoring System Started. Fetching initial data...")
run_system()

# Schedule to fetch data every 5 minutes
schedule.every(5).minutes.do(run_system)

# Run the scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)
