from unittest.mock import MagicMock

from django.test import TestCase

from weather.helpers import get_average_temp


class AverageTempTests(TestCase):
    def setUp(self):
        self.mock_service_10_degree = self.get_mock_service(10)
        self.mock_service_20_degree = self.get_mock_service(20)
        self.mock_service_30_degree = self.get_mock_service(30)

    def test_empty_list(self):
        service_providers = []
        value = get_average_temp(0, 0, service_providers)
        self.assertIsNone(value)

    def test_single_service(self):
        service_providers = [self.mock_service_10_degree]
        value = get_average_temp(0, 0, service_providers)
        self.assertEqual(value, 10)

    def test_three_services(self):
        service_providers = [self.mock_service_10_degree, self.mock_service_20_degree, self.mock_service_30_degree]
        value = get_average_temp(0, 0, service_providers)
        self.assertEqual(value, 20)

    @staticmethod
    def get_mock_service(temp_to_return: float) -> MagicMock:
        mock = MagicMock()
        mock.get_temp.return_value = temp_to_return
        return mock
