from datetime import datetime
from unittest import mock

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


class TestWeatherCheck(TestCase):
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

    def test_uses_current_date_as_start_date_if_start_date_not_specified(self):
        expected = {
            "data": [
                {
                    "date": "2023-11-01",
                    "sunrise": "2023-11-01T01:08",
                    "sunset": "2023-11-01T12:35",
                    "temperature_max": "35.2",
                    "temperature_min": "23.8",
                    "avg_rainfall_probability": "0",
                },
                {
                    "date": "2023-11-02",
                    "sunrise": "2023-11-02T01:09",
                    "sunset": "2023-11-02T12:34",
                    "temperature_max": "35.2",
                    "temperature_min": "23.4",
                    "avg_rainfall_probability": "0",
                },
                {
                    "date": "2023-11-03",
                    "sunrise": "2023-11-03T01:09",
                    "sunset": "2023-11-03T12:34",
                    "temperature_max": "35.6",
                    "temperature_min": "23.9",
                    "avg_rainfall_probability": "0",
                },
            ]
        }

        response = None

        now = datetime(2023, 11, 2)
        with mock.patch("clients.weather.requests.get") as mocked_get:
            mocked_get.return_value.raise_for_stats.return_value = None
            mocked_get.return_value.json.return_value = {
                "latitude": 19.125,
                "longitude": 72.875,
                "generationtime_ms": 0.03790855407714844,
                "utc_offset_seconds": 0,
                "timezone": "GMT",
                "timezone_abbreviation": "GMT",
                "elevation": 6.0,
                "daily_units": {
                    "time": "iso8601",
                    "temperature_2m_max": "°C",
                    "temperature_2m_min": "°C",
                    "sunrise": "iso8601",
                    "sunset": "iso8601",
                    "precipitation_probability_mean": "%",
                },
                "daily": {
                    "time": ["2023-11-01", "2023-11-02", "2023-11-03"],
                    "temperature_2m_max": [35.2, 35.2, 35.6],
                    "temperature_2m_min": [23.8, 23.4, 23.9],
                    "sunrise": [
                        "2023-11-01T01:08",
                        "2023-11-02T01:09",
                        "2023-11-03T01:09",
                    ],
                    "sunset": [
                        "2023-11-01T12:35",
                        "2023-11-02T12:34",
                        "2023-11-03T12:34",
                    ],
                    "precipitation_probability_mean": [0, 0, 0],
                },
            }

            with mock.patch("planner.services.get_current_date") as mocked_date:
                mocked_date.return_value = now.date()
                response = CLIENT.get(
                    reverse("weather_check"),
                    data={
                        "latitude": "19.0760",
                        "longitude": "72.8777",
                    },
                )

        assert response is not None
        assert response.status_code == 200
        assert response.json() == expected

    def test_returns_500_if_call_to_weather_service_fails(self):
        response = None
        with mock.patch("clients.weather.requests.get") as mocked_get:
            mocked_get.side_effect = Exception("random error")

            response = CLIENT.get(
                reverse("weather_check"),
                data={
                    "latitude": "19.0760",
                    "longitude": "72.8777",
                    "trip_date": "2023-12-25",
                },
            )

        assert response is not None
        assert response.status_code == 500
        assert response.json() == {"detail": "Internal Server Error"}

    def test_returns_correct_data_for_specified_parameters(self):
        expected = {
            "data": [
                {
                    "date": "2023-11-09",
                    "sunrise": "2023-11-09T01:08",
                    "sunset": "2023-11-09T12:35",
                    "temperature_max": "35.2",
                    "temperature_min": "23.8",
                    "avg_rainfall_probability": "0",
                },
                {
                    "date": "2023-11-10",
                    "sunrise": "2023-11-10T01:09",
                    "sunset": "2023-11-10T12:34",
                    "temperature_max": "35.2",
                    "temperature_min": "23.4",
                    "avg_rainfall_probability": "0",
                },
                {
                    "date": "2023-11-11",
                    "sunrise": "2023-11-11T01:09",
                    "sunset": "2023-11-11T12:34",
                    "temperature_max": "35.6",
                    "temperature_min": "23.9",
                    "avg_rainfall_probability": "0",
                },
            ]
        }

        with mock.patch("clients.weather.requests.get") as mocked_get:
            mocked_get.return_value.raise_for_stats.return_value = None
            mocked_get.return_value.json.return_value = {
                "latitude": 19.125,
                "longitude": 72.875,
                "generationtime_ms": 0.03790855407714844,
                "utc_offset_seconds": 0,
                "timezone": "GMT",
                "timezone_abbreviation": "GMT",
                "elevation": 6.0,
                "daily_units": {
                    "time": "iso8601",
                    "temperature_2m_max": "°C",
                    "temperature_2m_min": "°C",
                    "sunrise": "iso8601",
                    "sunset": "iso8601",
                    "precipitation_probability_mean": "%",
                },
                "daily": {
                    "time": ["2023-11-09", "2023-11-10", "2023-11-11"],
                    "temperature_2m_max": [35.2, 35.2, 35.6],
                    "temperature_2m_min": [23.8, 23.4, 23.9],
                    "sunrise": [
                        "2023-11-09T01:08",
                        "2023-11-10T01:09",
                        "2023-11-11T01:09",
                    ],
                    "sunset": [
                        "2023-11-09T12:35",
                        "2023-11-10T12:34",
                        "2023-11-11T12:34",
                    ],
                    "precipitation_probability_mean": [0, 0, 0],
                },
            }

            response = CLIENT.get(
                reverse("weather_check"),
                data={
                    "latitude": "19.0760",
                    "longitude": "72.8777",
                    "trip_date": "2023-11-10",
                },
            )

        assert response is not None
        assert response.status_code == 200
        assert response.json() == expected


class TestTripCreate:
    def setUp(self):
        # create a dummy user
        # create a dummy session
        # use that here
        pass

    def test_returns_400_if_locations_is_an_invalid_json(self):
        assert 1 == 0

    def test_returns_400_if_start_date_gt_end_date(self):
        assert 1 == 0

    def test_returns_400_if_start_date_in_past(self):
        assert 1 == 0

    def test_returns_400_if_end_date_in_past(self):
        assert 1 == 0

    def test_saves_trip_info_correctly(self):
        assert 1 == 0

    def test_returns_correct_response_for_saved_trip(self):
        assert 1 == 0
