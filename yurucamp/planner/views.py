from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

import pycountry

from planner.models import Location

# Create your views here.
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
