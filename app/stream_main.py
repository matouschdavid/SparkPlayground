import json
import time
import random
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, lit, when
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# OpenWeatherMap API details
API_KEY = "feaf45fe9858c60352278a74c4292598"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# List of cities to simulate weather data for
CITIES = [
    "New York", "London", "Berlin", "Tokyo", "Sydney",
    "Moscow", "Mumbai", "Cape Town", "Rio de Janeiro", "Beijing"
]

def fetch_weather(city):
    """Fetch weather data from OpenWeatherMap API for a single city."""
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        if response.status_code == 200:
            data = response.json()
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "weather": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"]
            }
        else:
            return None
    except Exception as e:
        print(f"Error fetching data for {city}: {e}")
        return None

def simulate_streaming_data():
    """Simulate streaming weather data by writing JSON lines to a file."""
    with open("/app/streaming_data/weather_stream.json", "w") as f:
        while True:
            city = random.choice(CITIES)
            weather_data = fetch_weather(city)
            if weather_data:
                f.write(json.dumps(weather_data) + "\n")
                f.flush()
            time.sleep(2)  # Simulate a 2-second delay between updates

def stream_main():
    import threading

    # Start the simulated streaming data generator in a separate thread
    threading.Thread(target=simulate_streaming_data, daemon=True).start()

    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("Stream Weather Processing") \
        .getOrCreate()

    # Define schema for incoming JSON data
    schema = StructType([
        StructField("city", StringType(), True),
        StructField("temperature", FloatType(), True),
        StructField("weather", StringType(), True),
        StructField("humidity", FloatType(), True)
    ])

    # Read streaming data
    streaming_df = spark.readStream \
        .schema(schema) \
        .json("/app/streaming_data/")

    # Perform transformations
    processed_df = streaming_df \
        .withColumn("extreme_weather",
                    when((col("temperature") > 35) | (col("temperature") < 0), lit("Yes")).otherwise(lit("No"))) \
        .withColumn("is_rainy", when(col("weather") == "Rain", lit("Yes")).otherwise(lit("No")))

    # Write processed data to console
    query = processed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    # Wait for the streaming query to finish
    query.awaitTermination()