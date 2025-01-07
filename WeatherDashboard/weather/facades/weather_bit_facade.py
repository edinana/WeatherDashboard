from ..services.weather_service import WeatherService
from django.conf import settings
import requests


class WeatherBitFacade(WeatherService):
    def __init__(self):
        self.base_url = settings.WEATHER_BIT_BASE_URL
        self.api_key = settings.WEATHER_BIT_API_KEY

    def fetch_weather_data(self, city):
        try:
            params = {
                "city": city,
                "key": self.api_key
            }
            response = requests.get(self.base_url, params=params)
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

                return weather_data
            else:
                print(f"WeatherBit: No data found for city {city}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from WeatherBit: {e}")
            return None