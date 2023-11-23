import json
import logging

import pycountry
from clients import OpenMeteoClient
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from helpers import get_current_date
from planner.models import Location, Trip
from planner.schema import Itinerary
from planner.services import WeatherCheckService
from pydantic import ValidationError

logger = logging.getLogger(__name__)


# since this data for this endpoint is not going to change very often, this is a great candidate for caching
# TODO: Consider implementing a local cache if there's enough time left over after writing the other endpoints
@require_http_methods(["GET"])
def list_locations(request):
    # no pagination because the example uses only 8 records
    # in a real world scenario, this endpoint would be paginated
    locations = Location.objects.order_by("country_code", "city_code")

    res = []
    for loc in locations:
        country = pycountry.countries.lookup(loc.country_code)
        res.append(
            {
                "country_display_name": country.name,
                "country_code": country.alpha_3,
                "city_code": loc.city_code,
                "city_display_name": loc.city_display_name,
                "city_coords": loc.city_coords,
            }
        )

    return JsonResponse(data={"data": res})


@require_http_methods(["GET"])
def weather_check(request):
    response = {}

    # ideally, this would come in from an env var
    # hardcoding it here in the interest of time
    weather_check_service = WeatherCheckService(
        client=OpenMeteoClient(url="https://api.open-meteo.com/v1/forecast")
    )
    try:
        response["data"] = weather_check_service.get_weather_info(
            lat=request.GET["latitude"],
            long=request.GET["longitude"],
            trip_date=request.GET.get("trip_date"),
        )
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"detail": "Internal Server Error"}, status=500)

    return JsonResponse(data=response)


@require_http_methods(["POST"])
def trips_handler(request):
    if request.method.upper() == "POST":
        return create_trip(request)


def create_trip(request):
    body = json.loads(request.body)
    try:
        data = Itinerary(**body["itinerary"])
    except ValidationError as e:
        res = {"detail": "Invalid trip format"}
        return JsonResponse(data=res, status=400)

    if data.start_date > data.end_date:
        return JsonResponse(
            data={"detail": "start_date cannot be greater than end date"}, status=400
        )

    user = request.user

    status = (
        Trip.TripStatus.DRAFT
        if body.get("is_draft", True)
        else Trip.TripStatus.PUBLISHED
    )

    trip = Trip(
        user_id=user.id,
        status=status.value,
        locations=json.loads(data.model_dump_json()),
    )
    trip.save()

    res = {
        "id": trip.gid,
        "locations": data.model_dump(),
    }

    return JsonResponse(data={"data": res}, status=201)
