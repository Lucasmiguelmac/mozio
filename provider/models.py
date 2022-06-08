from babel.numbers import list_currencies
from django.conf.global_settings import LANGUAGES
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

class ServiceArea(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=False)
    name = models.CharField(max_length=123, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=15, null=False)
    geojson = models.JSONField(null=False)

    class Meta:
        unique_together = ('provider', 'name')