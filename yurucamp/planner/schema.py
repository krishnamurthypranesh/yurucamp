from decimal import Decimal
from typing import List, Tuple

from pydantic import BaseModel, FutureDate


class CustomBase(BaseModel):
    pass


class ItineraryLocation(CustomBase):
    start_date: FutureDate
    end_date: FutureDate
    country: str
    city: str
    city_coords: Tuple[Decimal, Decimal]


class Itinerary(CustomBase):
    start_date: FutureDate
    end_date: FutureDate
    locations: List[ItineraryLocation]
