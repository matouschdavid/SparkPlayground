import requests
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, when, lit

# OpenWeatherMap API details
API_KEY = "feaf45fe9858c60352278a74c4292598"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# List of cities to fetch weather data for
CITIES = [
    "New York", "London", "Berlin", "Tokyo", "Sydney",
    "Moscow", "Mumbai", "Cape Town", "Rio de Janeiro", "Beijing"
]

def fetch_weather_data(cities):
    """Fetch weather data from OpenWeatherMap API for a list of cities."""
    weather_data = []
    for city in cities:
        try:
            response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
            if response.status_code == 200:
                data = response.json()
                weather_data.append({
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "weather": data["weather"][0]["main"],
                    "humidity": data["main"]["humidity"]
                })
            else:
                print(f"Failed to fetch data for {city}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")
    return weather_data

def batch_main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Batch Weather Analysis") \
        .getOrCreate()

    # Fetch weather data
    weather_data = fetch_weather_data(CITIES)

    # Convert data to Spark DataFrame
    weather_df = spark.createDataFrame(weather_data)

    # Display the raw data
    print("Raw Weather Data:")
    weather_df.show()

    # Calculate average temperature
    avg_temp_df = weather_df.groupBy("city").agg(
        avg("temperature").alias("avg_temperature")
    )
    print("Average Temperature per City:")
    avg_temp_df.show()

    # Identify cities with extreme weather conditions
    extreme_weather_df = weather_df.withColumn(
        "extreme_weather",
        when((col("temperature") > 35) | (col("temperature") < 0), lit("Yes")).otherwise(lit("No"))
    )
    print("Cities with Extreme Weather:")
    extreme_weather_df.filter(col("extreme_weather") == "Yes").show()

    # Group cities by weather condition
    weather_group_df = weather_df.groupBy("weather").count()
    print("Cities Grouped by Weather Condition:")
    weather_group_df.show()

    # Save results to CSV
    avg_temp_df.write.csv("/app/output/avg_temperature.csv", header=True)
    extreme_weather_df.write.csv("/app/output/extreme_weather.csv", header=True)
    weather_group_df.write.csv("/app/output/weather_groups.csv", header=True)

    print("Results saved to /app/output/")

    # Stop Spark session
    spark.stop()
