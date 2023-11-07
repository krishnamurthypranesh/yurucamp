from django.test import Client, TestCase
from django.urls import reverse

from planner.models import Location

CLIENT = Client()


class TestListLocations(TestCase):
    def setUp(self):
        Location.objects.all().delete()
        Location(
            **{
                "country_code": "IND",
                "city_code": "NEW_DELHI",
                "city_display_name": "New Delhi",
                "city_coords": ["28.6139", "77.2090"],
            }
        ).save()
        Location(
            **{
                "country_code": "IND",
                "city_code": "MUMBAI",
                "city_display_name": "Mumbai",
                "city_coords": ["19.0760", "72.8777"],
            }
        ).save()

    def test_returns_all_locations(self):
        response = CLIENT.get(
            reverse("list_locations"),
            headers={"key": "value"},
        )

        expected = {
            "data": [
                {
                    "country_display_name": "India",
                    "country_code": "IND",
                    "city_code": "MUMBAI",
                    "city_display_name": "Mumbai",
                    "city_coords": [
                        "19.0760000000",
                        "72.8777000000",
                    ],
                },
                {
                    "country_display_name": "India",
                    "country_code": "IND",
                    "city_code": "NEW_DELHI",
                    "city_display_name": "New Delhi",
                    "city_coords": ["28.6139000000", "77.2090000000"],
                },
            ]
        }

        assert response is not None
        assert response.status_code == 200
        assert response.json() == expected

    def test_returns_empty_list_if_db_table_is_empty(self):
        Location.objects.all().delete()

        response = CLIENT.get(
            reverse("list_locations"),
            headers={"key": "value"},
        )

        assert response is not None
        assert response.status_code == 200
        assert response.json() == {"data": []}
