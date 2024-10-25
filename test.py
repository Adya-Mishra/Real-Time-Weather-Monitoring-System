import unittest
from unittest.mock import patch
from data_processing import fetch_weather, aggregate_daily_data, process_and_store_data, kelvin_to_celsius
from alerting import check_thresholds
from config import ALERT_THRESHOLD, SPECIFIC_CONDITIONS, METROS
from datetime import datetime

class WeatherMonitoringSystemTests(unittest.TestCase):

    @patch('data_processing.requests.get')
    def test_fetch_weather(self, mock_get):
        # Mocking the API response
        mock_get.return_value.json.return_value = {
            "main": {
                "temp": 300.15,
                "feels_like": 302.15
            },
            "weather": [{"main": "Clear"}],
            "dt": 1638452400  # Example Unix timestamp
        }
        
        # Call the fetch_weather function
        city = "Delhi"
        result = fetch_weather(city)
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['city'], city)
        self.assertAlmostEqual(result['temp'], 27.0, places=1)  # 300.15 K to Celsius
        self.assertEqual(result['condition'], "Clear")

    def test_temperature_conversion(self):
        temp_k = 300.15
        expected_temp_c = 27.0  # 300.15 K to Celsius
        self.assertAlmostEqual(kelvin_to_celsius(temp_k), expected_temp_c, places=1)

    def test_daily_weather_summary(self):
        # Mocking daily data
        daily_data = {
            datetime.now().date(): [
                {"temp": 30.0, "condition": "Clear"},
                {"temp": 32.0, "condition": "Clear"},
                {"temp": 28.0, "condition": "Rain"}
            ]
        }

        with patch('data_processing.daily_data', daily_data):
            summary = aggregate_daily_data()
        
        self.assertIn("average_temp", summary)
        self.assertEqual(summary["average_temp"], 30.0)  # Average of the temperatures
        self.assertEqual(summary["max_temp"], 32.0)
        self.assertEqual(summary["min_temp"], 28.0)
        self.assertEqual(summary["dominant_condition"], "Clear")  # Most common condition

    def test_alerting_thresholds(self):
        # Test case with data above the threshold
        test_data = [
            {"city": "Delhi", "temp": 36.0, "condition": "Clear"},
            {"city": "Mumbai", "temp": 34.0, "condition": "Rain"}
        ]
        
        alerts = check_thresholds(test_data)
        self.assertIn("Alert: Temperature in Delhi is 36.00°C, which exceeds the threshold.", alerts)
        self.assertNotIn("Alert: Temperature in Mumbai is 34.00°C, which exceeds the threshold.", alerts)

        # Test case for specific conditions
        test_data_with_conditions = [
            {"city": "Delhi", "temp": 30.0, "condition": "Rain"},
            {"city": "Mumbai", "temp": 34.0, "condition": "Sunny"}
        ]
        
        alerts = check_thresholds(test_data_with_conditions)
        self.assertIn("Alert: Rain conditions detected in Delhi.", alerts)

    @patch('data_processing.store_daily_summary')
    @patch('data_processing.fetch_weather')
    def test_process_and_store_data(self, mock_fetch_weather, mock_store_daily_summary):
        # Mocking fetch_weather to return valid data for multiple cities
        mock_fetch_weather.side_effect = [
            {"city": "Delhi", "temp": 30.0, "feels_like": 31.0, "dt": datetime.now(), "condition": "Clear"},
            {"city": "Mumbai", "temp": 32.0, "feels_like": 33.0, "dt": datetime.now(), "condition": "Rain"},
            {"city": "Chennai", "temp": 29.0, "feels_like": 30.0, "dt": datetime.now(), "condition": "Sunny"},
            {"city": "Bangalore", "temp": 28.0, "feels_like": 29.0, "dt": datetime.now(), "condition": "Cloudy"},
            {"city": "Kolkata", "temp": 31.0, "feels_like": 32.0, "dt": datetime.now(), "condition": "Clear"},
            {"city": "Hyderabad", "temp": 27.0, "feels_like": 28.0, "dt": datetime.now(), "condition": "Sunny"},
        ]

        # Mocking store_daily_summary to always succeed
        mock_store_daily_summary.return_value = "Daily summary successfully stored in the database."

        # Call process_and_store_data function
        all_data, daily_summary, alerts, status_message = process_and_store_data()

        # Assertions
        self.assertEqual(status_message, "Daily summary successfully stored in the database.")
        self.assertEqual(len(all_data), len(METROS))  # Now we expect all cities in METROS

        # Check alerts contain rain conditions for Mumbai and clear conditions for Delhi or Kolkata
        self.assertIn("Alert: Rain conditions detected in Mumbai.", alerts)

if __name__ == '__main__':
    unittest.main()
