from babel.numbers import list_currencies
from django.conf.global_settings import LANGUAGES
from django.contrib.gis.db import models as geo_models
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Provider(models.Model):
    name = models.CharField(max_length=123)
    email = models.EmailField(max_length=123, unique=True)
    phone = PhoneNumberField()
    language = models.CharField(max_length=8, choices=LANGUAGES)
    currency = models.CharField(
        max_length=3, default="USD", choices=[(currency, currency) for currency in list_currencies()]
    )

class ServiceArea(geo_models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False, related_name="service_area")
    name = models.CharField(max_length=123, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=15, null=False)
    area = geo_models.PolygonField(null=True, srid=4326)

    class Meta:
        unique_together = ('provider', 'name')