import requests

from shipwell_interview.settings import NOAA_URL
from weather.apis.weather_source_base import WeatherSourceBase


class Noaa(WeatherSourceBase):
    @staticmethod
    def get_temp(latitude, longitude):
        data = Noaa.get_data_for_location(latitude, longitude)
        temp = data['today']['current']['fahrenheit']
        return int(temp)

    @staticmethod
    def get_data_for_location(latitude, longitude):
        url = NOAA_URL + f"noaa?latlon={latitude},{longitude}"
        request = requests.get(url)
        return request.json()
