from ..services.weather_service import WeatherService
from django.conf import settings
import requests


class OpenWeatherMapFacade(WeatherService):
    def __init__(self):
        self.base_url = settings.OPEN_WEATHER_MAP_BASE_URL
        self.units = settings.OPEN_WEATHER_MAP_UNITS
        self.api_key = settings.OPEN_WEATHER_MAP_API_KEY

    def fetch_weather_data(self, city):
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": self.units
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            weather_data = {
                'condition': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed']
            }

            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OpenWeatherMap: {e}")
            return None