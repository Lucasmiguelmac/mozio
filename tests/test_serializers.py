import pytest
from model_bakery import baker

from provider.api.serializers import (CreateUpdateServiceAreaSerializer,
                                      ProviderSerializer)
from provider.models import Provider, ServiceArea


class TestProviderSerializer:

    provider = baker.prepare(Provider, phone="+542494377777", email="test@email.com")

    def test_serialize(self):
        serializer = ProviderSerializer(self.provider)

        assert serializer.data

    def test_deserialize(self):
        provider_fields = [field.name for field in Provider._meta.get_fields()]
        valid_serialized_data = {
            k: v for (k, v) in self.provider.__dict__.items() if k in provider_fields and k != "id"
        } | {"phone": "+542494377777"}

        serializer = ProviderSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}


    @pytest.mark.parametrize("wrong_field", (
        {"phone": "a"},
        {"email": "breakingemail"},
        {"language": "breakinglanguage"},
        {"currency": "breakingcurrency"},
    ))
    def test_deserialize_fails(self, wrong_field: dict):
        provider_fields = [field.name for field in Provider._meta.get_fields()]
        valid_serialized_data = {
            k: v for (k, v) in self.provider.__dict__.items() if k in provider_fields and k != "id"
        } | {"phone": "+542494377777"} | wrong_field

        serializer = ProviderSerializer(data=valid_serialized_data)

        assert not serializer.is_valid()
        assert serializer.errors != {}

class TestCreateUpdateServiceAreaSerializer:

    service_area = baker.prepare(ServiceArea, provider_id=1)

    def test_serialize(self):
        serializer = CreateUpdateServiceAreaSerializer(self.service_area)

        assert serializer.data

    def test_deserialize(self):
        service_area_fields = [field.name for field in ServiceArea._meta.get_fields()]
        valid_serialized_data = {
            k: v for (k, v) in self.service_area.__dict__.items() if k in service_area_fields and k != "id"
        } | {"price": float(self.service_area.price)}

        serializer = CreateUpdateServiceAreaSerializer(data=valid_serialized_data)

        assert serializer.is_valid()
        assert serializer.errors == {}
