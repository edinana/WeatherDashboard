from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='weather_index'),
    path('weather/<str:city>/', views.weather_view, name='weather'),
    path('forecast/', views.forecast, name='forecast'),
]