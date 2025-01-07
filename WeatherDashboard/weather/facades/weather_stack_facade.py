from ..services.weather_service import WeatherService
from django.conf import settings
import requests


class WeatherStackFacade(WeatherService):
    def __init__(self):
        self.base_url = settings.WEATHER_STACK_BASE_URL
        self.api_key = settings.WEATHER_STACK_API_KEY

    def fetch_weather_data(self, city):
        try:
            params = {
                "access_key": self.api_key,
                "query": city
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            weather_data = {
                'condition': data['current']['weather_descriptions'][0],
                'temp': data['current']['temperature'],
                'humidity': data['current']['humidity'],
                'wind': data['current']['wind_speed']
            }

            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from WeatherStack: {e}")
            return None
