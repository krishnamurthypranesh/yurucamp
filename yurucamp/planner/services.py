from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

from clients import WeatherClientBase
import constants
from helpers import get_current_date


class WeatherCheckService:
    def __init__(self, client: WeatherClientBase):
        self.client = client

    # since this data for this endpoint is not going to change very often, this is a great candidate for caching
    # TODO: Consider implementing a local cache if there's enough time left over after writing the other endpoints
    def get_weather_info(self, lat: str, long: str, trip_date: Optional[str]):
        if not trip_date:
            trip_date = get_current_date()
        else:
            trip_date = datetime.fromisoformat(trip_date).date()

        start_date = trip_date - timedelta(days=1)
        end_date = trip_date + timedelta(days=1)

        data = self.client.get_weather_for_coords(
            lat=lat,
            long=long,
            start_date=str(start_date),
            end_date=str(end_date),
        )

        result = []
        for idx, dt in enumerate(data["dates"]):
            result.append(
                {
                    "date": dt,
                    "sunrise": data["sunrise"][idx],
                    "sunset": data["sunset"][idx],
                    "temperature_max": str(data["temperature_max"][idx]),
                    "temperature_min": str(data["temperature_min"][idx]),
                    "avg_rainfall_probability": str(
                        data["avg_rainfall_probability"][idx]
                    ),
                }
            )

        return result
