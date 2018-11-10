import requests

from shipwell_interview.settings import WEATHER_DOT_COM_URL
from weather.apis.weather_source_base import WeatherSourceBase


class WeatherDotCom(WeatherSourceBase):
    @staticmethod
    def get_temp(latitude, longitude):
        data = WeatherDotCom.get_data_for_location(latitude, longitude)
        temp = data['query']['results']['channel']['condition']['temp']
        return int(temp)

    @staticmethod
    def get_data_for_location(latitude, longitude):
        post_data = {
            'lat': latitude,
            'lon': longitude,
        }
        url = WEATHER_DOT_COM_URL + "weatherdotcom"
        request = requests.post(url, json=post_data)
        return request.json()
