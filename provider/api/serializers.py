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
        data["phone"] = str(instance.phone)
        return data


class ServiceAreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceArea


class CreateServiceAreaSerializer(serializers.ModelSerializer):
    provider_id = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta(ServiceAreaSerializer.Meta):
        exclude = ('id', 'provider')