from weather.apis.accuweather import Accuweather
from weather.apis.noaa import Noaa
from weather.apis.weather_com import WeatherDotCom

WEATHER_DATA_SOURCES = {
    'weather.com': {
        'api_class': WeatherDotCom,
        'display_name': "Weather.com",
        'mock_return_value': 25.0,
    },
    'noaa': {
        'api_class': Noaa,
        'display_name': "Noaa",
        'mock_return_value': 50.0,
    },
    'accuweather': {
        'api_class': Accuweather,
        'display_name': "Accuweather",
        'mock_return_value': 65.0,
    },
}
