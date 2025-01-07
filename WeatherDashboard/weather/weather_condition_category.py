from enum import Enum

class WeatherConditionCategory(Enum):
    CLOUDY = "Cloudy"
    SUNNY = "Sunny"
    RAINY = "Rainy"
    FOGGY = "Foggy"
    SNOWY = "Snowy"
    THUNDERSTORM = "Thunderstorm"
    CLEAR = "Clear"
    UNKNOWN = "Unknown"