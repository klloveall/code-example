class WeatherSourceBase:
    @staticmethod
    def get_temp(latitude: float, longitude: float) -> float:
        raise NotImplementedError
