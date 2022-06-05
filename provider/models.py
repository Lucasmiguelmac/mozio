from django.db import models
from languages.fields import LanguageField
from phonenumber_field.modelfields import PhoneNumberField


class Language(models.Model):
    name = models.CharField(max_length=100, blank=False)
    code = models.CharField(max_length=9, blank=False)


class Provider(models.Model):

    name = models.CharField(max_length=123, blank=False)
    email = models.EmailField(max_length=123, blank=False)

    phone = PhoneNumberField()
    language = LanguageField()
