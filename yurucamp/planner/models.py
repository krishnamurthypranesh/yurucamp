from datetime import datetime
import uuid

from django.db import models
from django.contrib.postgres import fields as pg_fields

from common import CustomBaseModel


class Location(CustomBaseModel):
    country_code = models.CharField(max_length=3, db_index=True)
    city_code = models.CharField(max_length=255)
    city_display_name = models.CharField(max_length=255)
    city_coords = pg_fields.ArrayField(
        base_field=models.DecimalField(null=False, decimal_places=10, max_digits=20),
        max_length=2,
    )

    class Meta:
        db_table = "locations"


class Trip(CustomBaseModel):
    class TripStatus(models.IntegerChoices):
        DRAFT = 10
        PUBLISHED = 20
        ONGOING = 30
        COMPLETED = 100

    # not a fan of using FKs since its a pain when sharding a database
    user_id = models.BigIntegerField(null=False)
    status = models.IntegerField(choices=TripStatus.choices)
    locations = models.JSONField(null=False)

    class Meta:
        db_table = "trips"
