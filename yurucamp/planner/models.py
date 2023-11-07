from django.db import models
from django.contrib.postgres import fields as pg_fields

from ksuid import Ksuid


class CustomBaseModel(models.Model):
    gid = models.UUIDField(default=Ksuid, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(models.Model):
    country_code = models.CharField(max_length=3, db_index=True)
    city_code = models.CharField(max_length=255)
    city_display_name = models.CharField(max_length=255)
    city_coords = pg_fields.ArrayField(
        base_field=models.DecimalField(null=False, decimal_places=10, max_digits=20),
        max_length=2,
    )

    class Meta:
        db_table = "locations"
