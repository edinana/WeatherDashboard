from .weather_service import WeatherService
import requests


class OpenWeatherMapFacade(WeatherService):
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_weather_data(self, city):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric'
        try:
            response = requests.get(url)
            data = response.json()
            weather_data = {
                'condition': data['weather'][0]['description'],
                'temp': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'wind': data['wind']['speed']
            }
            print("OPEN WEATHER")
            print(weather_data)
            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from OpenWeatherMap: {e}")
            return None