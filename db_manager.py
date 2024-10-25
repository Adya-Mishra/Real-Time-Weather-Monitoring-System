#db_manager.py
import pymysql.cursors
from config import DB_CONFIG
import pandas as pd


def connect_db():
    connection = pymysql.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

# Function to store daily summary
def store_daily_summary(daily_summary):
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                sql = """INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
                         VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    daily_summary["city"],           # Now includes city
                    daily_summary["date"],           # Now includes date
                    daily_summary["average_temp"],
                    daily_summary["max_temp"],
                    daily_summary["min_temp"],
                    daily_summary["dominant_condition"]
                ))
            connection.commit()
        return "Daily summary successfully stored in the database."
    except Exception as e:
        return f"Failed to store daily summary: {e}"


def fetch_daily_summary():
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM daily_summary WHERE date = CURDATE()"
                cursor.execute(sql)
                result = cursor.fetchall()  # Fetch all records for today's date
                
                if not result:
                    print("No daily summary found for today.")
                    return None  # Return None if no results
                
                return result  # Return results if found
    except pymysql.MySQLError as e:
        print(f"MySQL error fetching daily summary: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching daily summary: {e}")
        return None



# Function to fetch historical data
def fetch_historical_data():
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM daily_summary ORDER BY date DESC"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                # Convert date fields if necessary
                for record in result:
                    record['date'] = pd.to_datetime(record['date'])  # Safely converts strings to datetime
        return result
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return None
