from django.shortcuts import render
from .facades.open_weather_map_facade import OpenWeatherMapFacade
from .facades.weather_stack_facade import WeatherStackFacade
from .facades.weather_bit_facade import WeatherBitFacade
from .services.weather_data_fetcher import WeatherDataFetcher
from .services.forecast_service import ForecastService
from django.http import JsonResponse
import json


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
    weather_data_fetcher = WeatherDataFetcher([
        OpenWeatherMapFacade(),
        WeatherBitFacade()]
    )
    weather_data = weather_data_fetcher.fetch_data(city)

    return JsonResponse(weather_data)

def home(request):
    return render(request, 'weather/index.html')