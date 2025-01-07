from ..enums.weather_condition_category import WeatherConditionCategory
from datetime import timedelta, datetime
from collections import Counter
import numpy as np
import statistics


class Helper:
    def __init__(self):
       pass

    @staticmethod
    def get_datetime_range(target_date, time, delta_days=5):
        target_datetime = datetime.combine(target_date, time)
        return target_datetime - timedelta(days=delta_days), target_datetime + timedelta(days=delta_days)

    @staticmethod
    def get_weighted_average(data, similarities):
        return np.average(data, weights=similarities)

    @staticmethod
    def calculate_median(values):
        return statistics.median(values)

    @staticmethod
    def apply_majority_voting_for_categorical_data(values):
        return Counter(values).most_common(1)[0][0]

    @staticmethod
    def classify_conditions(conditions):
        return [Helper.classify_condition(condition) for condition in conditions]

    @staticmethod
    def classify_condition(condition):
        condition = condition.lower()
        if "cloud" in condition or "overcast" in condition:
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
