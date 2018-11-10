from functools import wraps
from typing import Dict
from unittest.mock import MagicMock

from django.test import TestCase
from django.urls import reverse

from weather.constants import WEATHER_DATA_SOURCES


def mock_weather_sources(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        classes = {}
        # Was going to mock these out, but this turned out to be way easier
        for api_name in WEATHER_DATA_SOURCES:
            classes[api_name] = WEATHER_DATA_SOURCES[api_name]['api_class']
            WEATHER_DATA_SOURCES[api_name]['api_class'] = MagicMock()
            WEATHER_DATA_SOURCES[api_name]['api_class'].get_temp.return_value = \
                WEATHER_DATA_SOURCES[api_name]['mock_return_value']

        func(*args, **kwargs)

        for api_name in classes:
            WEATHER_DATA_SOURCES[api_name]['api_class'] = classes[api_name]

    return wrap


class AverageTempApiTests(TestCase):
    """This function provides some helper functions; actual test functions are in classes below."""

    def assertSingleJsonError(self, request_variables: Dict, field_with_error: str, expected_error_message: str):
        response = self.client.get(reverse('weather_api'), request_variables)

        self.assertTrue('errors' in response.json(), "There are no errors! :(")

        errors = response.json()['errors']

        self.assertEqual(len(errors[field_with_error]),
                         1,
                         f"There should be only one error message for field `{field_with_error}`.")

        self.assertEqual(len(errors),
                         1,
                         f"There should be only one error message. \n Error messages are:\n{errors}")

        self.assertEqual(errors[field_with_error][0],
                         expected_error_message,
                         "Error message is incorrect.")

        self.assertEqual(response.status_code,
                         422,
                         "Error code 422 should be returned for syntactically correct but semantically incorrect calls.")


class SourceTests(AverageTempApiTests):
    @mock_weather_sources
    def test_accuweather_source(self):
        self.weather_source_test('accuweather')

    @mock_weather_sources
    def test_noaa_source(self):
        self.weather_source_test('noaa')

    @mock_weather_sources
    def test_weather_dot_com_source(self):
        self.weather_source_test('weather.com')

    @mock_weather_sources
    def test_all_sources(self):
        all_source_names = [k for k, x in WEATHER_DATA_SOURCES.items()]
        request = self.client.get(reverse('weather_api'),
                                  {'latitude': 0, 'longitude': 0, 'sources': all_source_names})

        self.assertEqual(request.status_code, 200)

        mock_values = [x['mock_return_value'] for k, x in WEATHER_DATA_SOURCES.items()]
        average_temp = sum(mock_values) / len(mock_values)

        self.assertEqual(request.json()['result']['average_temperature'], average_temp)

    def weather_source_test(self, source_name):
        request = self.client.get(reverse('weather_api'), {'latitude': 0, 'longitude': 0, 'sources': source_name})
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.json()['result']['average_temperature'],
                         WEATHER_DATA_SOURCES[source_name]['mock_return_value'])


class LatitudeErrorTests(AverageTempApiTests):
    def test_missing_latitude_returns_error(self):
        request_params = {'longitude': 0, 'sources': 'noaa'}
        self.assertSingleJsonError(request_params, 'latitude', 'This field is required.')

    def test_latitude_above_range_returns_error(self):
        request_params = {'latitude': 180.1, 'longitude': 0, 'sources': 'noaa'}
        self.assertSingleJsonError(request_params, 'latitude', 'Ensure this value is less than or equal to 180.')

    @mock_weather_sources
    def test_latitude_at_top_range_succeeds(self):
        request = self.client.get(reverse('weather_api'), {'latitude': 180.0, 'longitude': 0, 'sources': 'noaa'})
        self.assertEqual(request.status_code, 200)

    def test_latitude_below_range_returns_error(self):
        request_params = {'latitude': -180.1, 'longitude': 0, 'sources': 'noaa'}
        self.assertSingleJsonError(request_params, 'latitude', 'Ensure this value is greater than or equal to -180.')

    @mock_weather_sources
    def test_latitude_at_bottom_range_succeeds(self):
        request = self.client.get(reverse('weather_api'), {'latitude': -180.0, 'longitude': 0, 'sources': 'noaa'})
        self.assertEqual(request.status_code, 200)


class LongitudeErrorTests(AverageTempApiTests):
    def test_missing_longitude_returns_error(self):
        request_params = {'latitude': 0, 'sources': 'noaa'}
        self.assertSingleJsonError(request_params, 'longitude', 'This field is required.')

    def test_longitude_above_range_returns_error(self):
        request_params = {'latitude': 0, 'longitude': 90.1, 'sources': 'noaa'}
        self.assertSingleJsonError(request_params, 'longitude', 'Ensure this value is less than or equal to 90.')

    @mock_weather_sources
    def test_longitude_at_top_range_succeeds(self):
        request = self.client.get(reverse('weather_api'), {'latitude': 0, 'longitude': 90, 'sources': 'noaa'})
        self.assertEqual(request.status_code, 200)

    def test_longitude_below_range_returns_error(self):
        request_params = {'latitude': 0, 'longitude': -90.1, 'sources': 'noaa'}
        self.assertSingleJsonError(request_params, 'longitude', 'Ensure this value is greater than or equal to -90.')

    @mock_weather_sources
    def test_longitude_at_bottom_range_succeeds(self):
        request = self.client.get(reverse('weather_api'), {'latitude': 0, 'longitude': -90, 'sources': 'noaa'})
        self.assertEqual(request.status_code, 200)


class SourceErrorTests(AverageTempApiTests):
    def test_missing_source_selection_returns_error(self):
        request_params = {'latitude': 0, 'longitude': 0}
        self.assertSingleJsonError(request_params, 'sources', 'This field is required.')
