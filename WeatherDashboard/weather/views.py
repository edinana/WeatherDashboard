import os
from django.shortcuts import render
from django.core.cache import cache
from .open_weather_map_facade import OpenWeatherMapFacade
from .weather_stack_facade import WeatherStackFacade
from .weather_bit_facade import WeatherBitFacade
from .weather_data_fetcher import WeatherDataFetcher
from .forecast_service import ForecastService
from django.http import JsonResponse
import json

OPEN_WEATHER_MAP_API_KEY = os.getenv('OPEN_WEATHER_MAP_API_KEY')
WEATHER_STACK_API_KEY = os.getenv('WEATHER_STACK_API_KEY')
WEATHER_BIT_API_KEY = os.getenv('WEATHER_BIT_API_KEY')
service_confidence_scores = {
    "OpenWeatherMap": 0.8,
    "WeatherStack": 0.6,
    "WeatherBit": 0.7,
}


def get_weather_data(city):
    cache_key = f"weather_data_{city}"
    cached_data = cache.get(cache_key)

    if cached_data:
        print(f"Returning cached data for {city}")
        return cached_data

    open_weather_map_facade = OpenWeatherMapFacade(OPEN_WEATHER_MAP_API_KEY)
    weather_stack_facade = WeatherStackFacade(WEATHER_STACK_API_KEY)
    weather_bit_facade = WeatherBitFacade(WEATHER_BIT_API_KEY)

    weather_data_fetcher = WeatherDataFetcher(
        [open_weather_map_facade, weather_stack_facade, weather_bit_facade],
        service_confidence_scores
    )

    weather_data = weather_data_fetcher.fetch_data(city)

    if weather_data:
        cache.set(cache_key, weather_data, timeout=3600)
    else:
        weather_data = {"error": "Unable to fetch weather data"}

    return weather_data

def forecast(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        city = data.get('city')
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        wind_speed = data.get('wind_speed')
        condition = data.get('condition')

        forecast_service = ForecastService(city, temperature, humidity, wind_speed, condition)
        forecast_data = forecast_service.predict()

        return JsonResponse({'forecast': forecast_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def weather_view(request, city):
    weather_data = get_weather_data(city)
    return JsonResponse(weather_data)

def home(request):
    return render(request, 'weather/index.html')