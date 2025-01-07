from collections import Counter
from .weather_condition_category import WeatherConditionCategory
import statistics

class WeatherDataFetcher:
    def __init__(self, services: list, service_confidence_scores: dict):
        self.services = services
        self.service_confidence_scores = service_confidence_scores

    def fetch_data(self, city):
        weather_data = []

        for service in self.services:
            service_data = service.fetch_weather_data(city)
            if service_data:
                weather_data.append(service_data)

        if len(weather_data) > 0:
            return self.combine_weather_data(weather_data)
        else:
            return None

    def decide_numerical_value(self, weighted_average, median):
        if abs(weighted_average - median) / max(weighted_average, median) <= 0.05:
            return weighted_average
        else:
            return median

    def calculate_weighted_average(self, values):
        total_weight = 0
        weighted_sum = 0

        for i, value in enumerate(values):
            service_name = list(self.service_confidence_scores.keys())[i]
            weight = self.service_confidence_scores.get(service_name, 1)
            total_weight += weight
            weighted_sum += value * weight

        return weighted_sum / total_weight if total_weight != 0 else None

    def calculate_median(self, values):
        return statistics.median(values)

    def classify_condition(self, condition):
        condition = condition.lower()
        if "cloud" in condition:
            return WeatherConditionCategory.CLOUDY
        elif "sun" in condition:
            return WeatherConditionCategory.SUNNY
        elif "clear" in condition:
            return WeatherConditionCategory.CLEAR
        elif "rain" in condition or "drizzle" in condition:
            return WeatherConditionCategory.RAINY
        elif "fog" in condition:
            return WeatherConditionCategory.FOGGY
        elif "snow" in condition:
            return WeatherConditionCategory.SNOWY
        elif "thunder" in condition or "storm" in condition:
            return WeatherConditionCategory.THUNDERSTORM
        else:
            return WeatherConditionCategory.UNKNOWN

    def classify_conditions(self, conditions):
        return [self.classify_condition(condition) for condition in conditions]

    def apply_majority_voting_for_categorical_data(self, values):
        return Counter(values).most_common(1)[0][0]

    def combine_weather_data(self, weather_data):
        combined_data = {}

        for key in weather_data[0].keys():
            values = [data[key] for data in weather_data]

            if isinstance(values[0], (int, float)):
                weighted_average = self.calculate_weighted_average(values)
                median_value = self.calculate_median(values)

                combined_data[key] = self.decide_numerical_value(weighted_average, median_value)
            else:
                conditions = self.classify_conditions(values)
                combined_data[key] = self.apply_majority_voting_for_categorical_data(conditions).value

        return combined_data
