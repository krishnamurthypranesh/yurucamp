import uuid
from datetime import datetime
from unittest import TestCase, mock

import pytest
from authn import models as auth_models
from django.test import Client, TestCase
from django.urls import reverse
from planner.models import Location, Trip

from yurucamp.settings import env

# pytestmark = pytest.mark.django_db


class TestsBase:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, request, db, setup_user_account):
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

        self.client = Client()

        username, password = setup_user_account

        response = self.client.post(
            reverse("create_session"),
            json={
                "username": username,
                "password": password,
            },
            headers={"Content-Type": "application/json"},
        )
        breakpoint()
        assert response is not None
        assert response.status_code == 200
        self.token = response.json()["token"]


@pytest.mark.django_db
class TestListLocations(TestsBase):
    @pytest.mark.django_db
    def test_returns_all_locations(self):
        response = self.client.get(
            reverse("list_locations"),
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

        response = self.client.get(
            reverse("list_locations"),
        )

        assert response is not None
        assert response.status_code == 200
        assert response.json() == {"data": []}

    def test_returns_401_if_user_is_unauthenticated(self):
        c = Client()

        response = c.get(
            reverse("list_locations"),
        )

        assert response is not None
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"


class TestWeatherCheck(TestCase):
    def setUp(self):
        self.client = Client()

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

        self.username = f"john-{str(uuid.uuid1()).split('-')[0]}"
        self.password = "pass1234"

        user = auth_models.User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.user = user

        self.client.login(username=self.username, password=self.password)

    def test_returns_401_if_user_is_unauthenticated(self):
        c = Client()

        response = c.get(
            reverse("weather_check"),
        )

        assert response is not None
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"

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
                response = self.client.get(
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

            response = self.client.get(
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

            response = self.client.get(
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


class TestTripCreate(TestCase):
    def setUp(self):
        self.client = Client()

        self.username = f"john-{str(uuid.uuid1()).split('-')[0]}"
        self.password = "pass1234"

        user = auth_models.User.objects.create_user(
            username=self.username,
            password=self.password,
        )

        self.user = user

        self.client.login(username=self.username, password=self.password)

        self.itinerary = {
            "start_date": "2023-11-11",
            "end_date": "2023-11-21",
            "locations": [
                {
                    "start_date": "2023-11-11",
                    "end_date": "2023-11-21",
                    "country": "IND",
                    "city": "MUMBAI",
                    "city_coords": ["22.0000", "22.0000"],
                }
            ],
        }

    def test_returns_401_if_user_is_unauthenticated(self):
        c = Client()

        response = c.post(
            reverse("trips"),
            data={
                "itinerary": {},
            },
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 401
        assert response.json()["detail"] == "Unauthorized"

    def test_returns_400_if_locations_is_an_invalid_json(self):
        response = self.client.post(
            reverse("trips"),
            data={
                "itinerary": {},
            },
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid trip format"

    def test_returns_400_if_start_date_gt_end_date(self):
        self.itinerary["start_date"] = "2023-11-22 00:00:00"

        response = self.client.post(
            reverse("trips"),
            data={
                "itinerary": self.itinerary,
            },
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 400
        assert response.json()["detail"] == "start_date cannot be greater than end date"

    def test_saves_trip_info_correctly(self):
        response = self.client.post(
            reverse("trips"),
            data={
                "itinerary": self.itinerary,
            },
            content_type="application/json",
        )

        assert response is not None
        assert response.status_code == 201

        response = response.json()

        trip = Trip.objects.get(gid=response["data"]["id"])

        assert trip is not None
        assert trip.status == Trip.TripStatus.DRAFT.value
        assert trip.user_id == self.user.id
        TestCase().assertDictEqual(trip.locations, self.itinerary)
