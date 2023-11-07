from decimal import Decimal
from typing import Tuple

from pydantic import BaseModel, AwareDatetime


class CustomBase(BaseModel):
    pass


class ItineraryLocation(CustomBase):
    start_time: AwareDatetime
    end_time: AwareDatetime
    country: str
    city: str
    city_coords: Tuple[Decimal, Decimal]


class Itinerary(CustomBase):
    start_time: AwareDatetime
    end_time: AwareDatetime
    locations: [ItineraryLocation]
