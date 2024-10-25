# alerting.py
from config import SPECIFIC_CONDITIONS

def check_thresholds(data, alert_threshold):
    alerts = []
    for entry in data:
        temp = entry.get("temp", None)
        condition = entry.get("condition", None)

        # Ensure the temperature is a valid number
        if temp is not None and isinstance(temp, (int, float)):
            if temp > alert_threshold:
                alerts.append(f"Alert: Temperature in {entry['city']} is {temp:.2f}°C, which exceeds the threshold.")

        # Check for specific conditions
        if condition in SPECIFIC_CONDITIONS:
            alerts.append(f"Alert: {condition} conditions detected in {entry['city']}.")

    return alerts
