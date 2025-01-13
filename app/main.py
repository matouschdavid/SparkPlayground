from pyspark.sql import SparkSession
from openweather_utils import fetch_weather_data

from pyspark.sql import SparkSession

def main():
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("OpenWeather Spark App") \
        .getOrCreate()

    # Fetch real-time weather data
    weather_data = fetch_weather_data()

    # Process weather data using Spark
    df = spark.createDataFrame(weather_data)
    df.show()

    # Example: Filtering data
    warm_df = df.filter(df.temp > 3)
    warm_df.show()

    cold_df = df.filter(df["temp"] <= 3)
    cold_df.show()

    union_df = warm_df.union(cold_df)
    union_df.show()

    # Stop Spark session
    spark.stop()


if __name__ == "__main__":
    main()
