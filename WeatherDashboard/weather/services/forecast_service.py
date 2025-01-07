from sklearn.metrics.pairwise import cosine_similarity
from datetime import timedelta, datetime
from ..models import WeatherData
from ..helpers.helpers import Helper
import numpy as np


class ForecastService:
    def __init__(self, city, temperature, humidity, wind_speed, condition):
        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.condition = condition

    def get_historical_data(self, date, time):
        historical_data = []
        previous_4_years = [date.year - i for i in range(1, 5)]
        for year in previous_4_years:
            # same day in previous years
            target_date = date.replace(year=year)

            target_datetime_start, target_datetime_end = Helper.get_datetime_range(target_date, time)

            data_for_year = WeatherData.objects.filter(
                city_name=self.city,
                datetime__gte=target_datetime_start,
                datetime__lte=target_datetime_end
            ).order_by('datetime')

            for record in data_for_year:
                if record.datetime.time() == time:
                    historical_data.append([
                        record.temperature,
                        record.wind_speed,
                        record.humidity,
                        record.weather_description])

        return historical_data

    def predict(self):
        current_vector = np.array([self.temperature, self.wind_speed, self.humidity]).reshape(1, -1)

        # get the beginning of the hour
        current_datetime = datetime.now()
        current_time = datetime.time(current_datetime.replace(hour=current_datetime.hour, minute=0, second=0, microsecond=0))

        current_hour_historical_data = self.get_historical_data(current_datetime.date(), current_time)

        historical_vectors = np.array([[data[0], data[1], data[2]] for data in current_hour_historical_data])
        similarities = cosine_similarity(current_vector, historical_vectors).flatten()

        one_hour_from_now = current_datetime + timedelta(hours=1)
        next_hour_time = one_hour_from_now.replace(minute=0, second=0, microsecond=0).time()
        following_hour_historical_data = self.get_historical_data(one_hour_from_now.date(), next_hour_time)

        weighted_avg_temperature = Helper.get_weighted_average(
            [data[0] for data in following_hour_historical_data], similarities)
        weighted_avg_wind_speed = Helper.get_weighted_average(
            [data[1] for data in following_hour_historical_data], similarities)
        weighted_avg_humidity = Helper.get_weighted_average(
            [data[2] for data in following_hour_historical_data], similarities)

        conditions = [data[3] for data in following_hour_historical_data]
        classified_conditions = Helper.classify_conditions(conditions)
        majority_condition = Helper.apply_majority_voting_for_categorical_data(classified_conditions).value

        return {
            "forecast_temperature": weighted_avg_temperature,
            "forecast_wind_speed": weighted_avg_wind_speed,
            "forecast_humidity": weighted_avg_humidity,
            "forecast_condition": majority_condition
        }