from django.db import models


class WeatherData(models.Model):
    city_name = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    temperature = models.FloatField(null=True, blank=True)
    weather_description = models.TextField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'weather_data'
        constraints = [
            models.UniqueConstraint(fields=['city_name', 'datetime'], name='unique_weather_data')
        ]
        indexes = [
            models.Index(fields=['city_name'], name='idx_city_name')
        ]