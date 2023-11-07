from abc import abstractmethod
from decimal import Decimal

import requests

import constants

METRICS = [
    constants.OPEN_METEO_SUNRISE,
    constants.OPEN_METEO_SUNSET,
    constants.OPEN_METEO_TEMPERATURE_MAX,
    constants.OPEN_METEO_TEMPERATURE_MIN,
    constants.OPEN_METEO_AVG_RAINFALL_PROBABILITY,
]


class WeatherClientBase:
    def __init__(self, url: str, *args, **kwargs):
        self.url = url

    @abstractmethod
    def get_weather_for_coords(
        self, lat: Decimal, long: Decimal, start_date: str, end_date: str
    ):
        pass


class OpenMeteoClient(WeatherClientBase):
    def get_weather_for_coords(
        self, lat: Decimal, long: Decimal, start_date: str, end_date: str
    ):
        params = {
            "latitude": lat,
            "longitude": long,
            "daily": METRICS,
            "start_date": start_date,
            "end_date": end_date,
        }

        response = requests.get(
            url=self.url,
            params=params,
        )

        # open-meteo raises an error if the dates outside of a specified range
        # ideally, this'll need to be handled and a 400 should be returned to the user
        # letting them know what's possible, but since I'm lacking time, I'm going with returning a generic error
        response.raise_for_status()

        response = response.json()

        return {
            "dates": response["daily"]["time"],
            "temperature_max": response["daily"][constants.OPEN_METEO_TEMPERATURE_MAX],
            "temperature_min": response["daily"][constants.OPEN_METEO_TEMPERATURE_MIN],
            "avg_rainfall_probability": response["daily"][
                constants.OPEN_METEO_AVG_RAINFALL_PROBABILITY
            ],
            "sunrise": response["daily"]["sunrise"],
            "sunset": response["daily"]["sunset"],
        }
