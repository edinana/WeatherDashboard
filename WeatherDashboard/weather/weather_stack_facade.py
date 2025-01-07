from .weather_service import WeatherService
import requests


class WeatherStackFacade(WeatherService):
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather_data(self, city):
        url = f'https://api.weatherstack.com/current?access_key={self.api_key}&query={city}'
        try:
            response = requests.get(url)
            data = response.json()
            weather_data = {
                'condition': data['current']['weather_descriptions'][0],
                'temp': data['current']['temperature'],
                'humidity': data['current']['humidity'],
                'wind': data['current']['wind_speed']
            }
            print("Weather Stack")
            print(weather_data)
            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from WeatherStack: {e}")
            return None
