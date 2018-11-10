from typing import List

from weather.apis.weather_source_base import WeatherSourceBase


def get_average_temp(latitude: float, longitude: float, service_providers: List[WeatherSourceBase]) -> float or None:
    if not service_providers:
        return None

    sum_temp = 0
    for api_class in service_providers:
        sum_temp += float(api_class.get_temp(latitude, longitude))

    average_temp = sum_temp / len(service_providers)

    return average_temp
