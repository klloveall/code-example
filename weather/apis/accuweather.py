import requests

from shipwell_interview.settings import ACCUWEATHER_URL
from weather.apis.weather_source_base import WeatherSourceBase


class Accuweather(WeatherSourceBase):
    @staticmethod
    def get_temp(latitude, longitude):
        data = Accuweather.get_data_for_location(latitude, longitude)
        temp = data['simpleforecast']['forecastday'][0]['current']['fahrenheit']
        return int(temp)

    @staticmethod
    def get_data_for_location(latitude, longitude):
        url = ACCUWEATHER_URL + f"accuweather?latitude={latitude}&longitude={longitude}"
        request = requests.get(url)
        return request.json()
