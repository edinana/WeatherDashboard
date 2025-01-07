from ..helpers.helpers import Helper
from django.core.cache import cache
from django.conf import settings
from ..models import WeatherData
from datetime import datetime


class WeatherDataFetcher:
    def __init__(self, services: list):
        self.services = services
        self.service_confidence_scores = settings.SERVICE_CONFIDENCE_SCORES

    def fetch_data(self, city):
        cache_key = f"weather_data_{city}"
        cached_data = cache.get(cache_key)

        if cached_data:
            print(f"Returning cached data for {city}")
            return cached_data

        weather_data = []

        for service in self.services:
            service_data = service.fetch_weather_data(city)
            if service_data:
                weather_data.append(service_data)

        if len(weather_data) > 0:
            combined_weather_data = self.combine_weather_data(weather_data)
            cache.set(cache_key, combined_weather_data, timeout=3600)

            WeatherData.objects.create(
                city_name=city,
                datetime=datetime.now().replace(minute=0, second=0, microsecond=0),
                temperature=round(combined_weather_data['temp'], 1),
                humidity=round(combined_weather_data['humidity']),
                wind_speed=round(combined_weather_data['wind'], 2),
                weather_description=combined_weather_data['condition']
            )

            return combined_weather_data
        else:
            return None

    def combine_weather_data(self, weather_data):
        combined_data = {}

        for key in weather_data[0].keys():
            values = [data[key] for data in weather_data]

            if isinstance(values[0], (int, float)):
                weights = [self.service_confidence_scores.get(list(self.service_confidence_scores.keys())[i], 1) for i
                           in range(len(values))]

                weighted_average = Helper.get_weighted_average(values, weights)
                median_value = Helper.calculate_median(values)

                combined_data[key] = self.decide_numerical_value(weighted_average, median_value)
            else:
                conditions = Helper.classify_conditions(values)
                combined_data[key] = Helper.apply_majority_voting_for_categorical_data(conditions).value

        return combined_data

    def decide_numerical_value(self, weighted_average, median):
        if abs(weighted_average - median) / max(weighted_average, median) <= 0.05:
            return weighted_average
        else:
            return median
