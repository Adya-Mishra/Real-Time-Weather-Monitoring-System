# Real-Time-Weather-Monitoring-System

## Overview
The Real-Time Weather Monitoring System is designed to fetch, process, and visualize weather data from various metropolitan cities in India. It monitors specific weather conditions and sends alerts based on temperature thresholds. The system includes functionalities for real-time updates, daily summaries, and historical data visualization.

## Features
- Fetches real-time weather data for selected Indian metros (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad).
- Monitors specific weather conditions (e.g., Rain, Snow) and triggers alerts when predefined temperature thresholds are exceeded.
- Stores daily weather summaries in a MySQL database for retrieval and analysis.
- Provides a user-friendly interface using Streamlit for displaying current weather data, daily summaries, and historical trends.
- Implements automated data fetching at regular intervals (every 5 minutes by default).

## Technologies Used
- Python
- Streamlit (for UI)
- MySQL (for database storage)
- Requests (for API calls)
- Plotly (for data visualization)
- Unittest (for testing)

## Setup Instructions

### Prerequisites
- Python 3.6 or higher
- MySQL Server
- An OpenWeatherMap API key (sign up at OpenWeatherMap to get your API key)

### Installation
1. Clone the repository:
   
     ```bash
     git clone https://github.com/yourusername/weather-monitoring-system.git
     cd weather-monitoring-system

2. Install required packages:

    ```bash
    pip install -r requirements.txt

3. Configure the database:
- Create a MySQL database named weather_data.
- Create a table named daily_summary with the following structure:
  
    ```sql
    CREATE TABLE daily_summary (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(50),
        date DATE,
        avg_temp FLOAT,
        max_temp FLOAT,
        min_temp FLOAT,
        dominant_condition VARCHAR(50)
    );
   
4. Update the config.py file:
- Set your API_KEY, database configuration (DB_CONFIG), and any specific conditions you want to monitor.

### Running the Application
1. Start the system:

    ```bash
    python main.py

This will fetch the weather data immediately and continue to run every 5 minutes.

2. For the user interface, run:

    ```bash
    streamlit run ui.py

## Usage
- Use the sidebar in the Streamlit app to configure your weather monitoring preferences, including setting the temperature alert threshold and update interval.
- Click the "Fetch Current Weather Data" button to retrieve the latest weather information and view the current weather summary.
- Access today’s summary and historical data directly from the app.
  
## Testing
To run unit tests, execute:

     python -m unittest discover -s tests
  
## License
This project is licensed under the MIT License. See the LICENSE file for details.

