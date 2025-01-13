import requests

API_KEY = "feaf45fe9858c60352278a74c4292598"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data():
    # Replace with cities or locations of interest
    cities = ["London", "New York", "Berlin", "Linz", "Cosenza", "Rome"]
    weather_data = []

    for city in cities:
        response = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": "metric"})
        if response.status_code == 200:
            data = response.json()
            weather_data.append({
                "city": city,
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"]
            })
        else:
            print(f"Failed to fetch data for {city}. Status code: {response.status_code}")

    return weather_data
