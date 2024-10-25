# ui.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from data_processing import process_and_store_data
from alerting import check_thresholds
from db_manager import fetch_daily_summary, fetch_historical_data

# Set Streamlit page configuration
st.set_page_config(
    page_title="Real-Time Weather Monitoring System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page Title
st.title("Real-Time Weather Monitoring System")
st.write("Get real-time weather updates, daily summaries, alerts, and historical trends.")

# Define update interval (in minutes) and threshold (in Celsius)
UPDATE_INTERVAL = 5  # Adjust as needed
ALERT_THRESHOLD = 35  # Change this to configure temperature alert threshold

# Sidebar configuration
st.sidebar.header("Settings")
st.sidebar.write("Configure your weather monitoring preferences:")
alert_threshold = st.sidebar.slider("Temperature Alert Threshold (°C)", 0, 50, ALERT_THRESHOLD)
update_interval = st.sidebar.slider("Update Interval (minutes)", 1, 30, UPDATE_INTERVAL)

# Initialize current data and daily summary
current_data = None
daily_summary = None

# Button to start real-time data fetching
if st.button("Fetch Current Weather Data"):
    current_data, daily_summary, alerts, status_message = process_and_store_data(alert_threshold)
    
    # Display storage status message
    st.info(status_message)

    # Display daily summary if available
    if daily_summary:
        st.subheader("Current Weather Summary")
        st.table(pd.DataFrame([daily_summary]))

# Separate section to fetch and display today's summary again
st.subheader("Today's Weather Summary")
try:
    daily_summary_from_db = fetch_daily_summary()  # Fetch from DB
    if daily_summary_from_db:
        # Display only the latest 5 records
        df_summary = pd.DataFrame(daily_summary_from_db).tail(5)
        st.table(df_summary)
    else:
        st.warning("No daily summary available for today.")
except Exception as e:
    st.error(f"Error fetching daily summary: {str(e)}")

# Display real-time data
st.subheader("Current Weather Data")
try:
    if current_data:  # Use current_data from previous call
        # Display only the latest 5 records
        for city_data in current_data[-5:]:  # Show the latest 5 records
            city = city_data.get('city', 'Unknown City')
            temp = city_data.get('temp', 'N/A')
            feels_like = city_data.get('feels_like', 'N/A')
            condition = city_data.get('condition', 'Condition Unknown')
            st.write(f"{city}: {temp}°C (Feels like {feels_like}°C), Condition: {condition}")

    else:
        st.warning("No current weather data available.")
except Exception as e:
    st.error(f"Error fetching current data: {str(e)}")

# Display daily summary
st.subheader("Daily Weather Summary")
try:
    daily_summary = fetch_daily_summary()
    if daily_summary:
        # Display only the latest 5 records
        df_summary = pd.DataFrame(daily_summary).tail(5)
        st.table(df_summary)
    else:
        st.warning("No daily summary available for today.")
except Exception as e:
    st.error(f"Error fetching daily summary: {str(e)}")

# Visualize historical data
st.subheader("Historical Weather Trends")
try:
    historical_data = fetch_historical_data()
    if historical_data:
        df_historical = pd.DataFrame(historical_data)
        df_historical['datetime'] = pd.to_datetime(df_historical['date'], unit='s')
        
        # Line chart for temperature trend
        fig = px.line(df_historical, x='datetime', y='avg_temp', color='city', title="Temperature Trend Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        # Bar chart for dominant weather condition count
        condition_counts = df_historical['dominant_condition'].value_counts().reset_index()
        condition_counts.columns = ['Condition', 'Count']

        # Plot the bar chart using the correct column names
        fig2 = px.bar(condition_counts, x='Condition', y='Count', title="Dominant Weather Conditions", labels={'Condition': 'Weather Condition', 'Count': 'Occurrence'})
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Error fetching historical data: {e}")

# Display alerts
st.subheader("Alerts")
try:
    if current_data:
        alerts = check_thresholds(current_data, alert_threshold)  # Pass the alert threshold here
        if alerts:
            st.write("Alerts triggered:")
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("No alerts triggered; all temperatures are below the threshold.")
    else:
        st.warning("No current weather data available to check alerts.")
except Exception as e:
    st.error(f"Error checking alerts: {str(e)}")

fetch_daily_summary()