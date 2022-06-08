from django.core.validators import EmailValidator, MaxLengthValidator
from rest_framework import serializers

from provider.models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Provider
        exclude = ('id',)
        extra_kwargs = {
            'email': {
                'validators': [MaxLengthValidator, EmailValidator]
            }
        }

    def to_representation(self, instance: Provider):
        data = super().to_representation(instance)
        if data.get("phone", False):
            data["phone"] = str(data["phone"])
        return data


class ServiceAreaSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())

    class Meta:
        model = ServiceArea
        read_only_fields = ('id',)
        fields = ('provider', 'name', 'price', 'geojson')
