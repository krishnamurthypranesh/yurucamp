import logging

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import pycountry

from clients import OpenMeteoClient
from planner.models import Location
from planner.services import WeatherCheckService

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
