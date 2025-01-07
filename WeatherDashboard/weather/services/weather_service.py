from abc import ABC, abstractmethod


class WeatherService(ABC):
    @abstractmethod
    def fetch_weather_data(self, city):
        pass