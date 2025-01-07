from .weather_service import WeatherService
import requests


class WeatherBitFacade(WeatherService):
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather_data(self, city):
        url = f'https://api.weatherbit.io/v2.0/current?city={city}&key={self.api_key}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "data" in data and len(data["data"]) > 0:
                weather_info = data["data"][0]
                weather_data = {
                    "condition": weather_info["weather"]["description"],
                    "temp": weather_info['temp'],
                    "humidity": weather_info["rh"],
                    "wind": weather_info['wind_spd']
                }
                print("WEATHER BIT")
                print(weather_data)
                return weather_data
            else:
                print(f"WeatherBit: No data found for city {city}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from WeatherBit: {e}")
            return None