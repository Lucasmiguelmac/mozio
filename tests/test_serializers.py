import pytest
from model_bakery import baker

from provider.api.serializers import ProviderSerializer
from provider.models import Provider


class TestProviderSerializer:

    def test_serialize(self):
        provider = baker.prepare(Provider, phone="+542494377777")
        serializer = ProviderSerializer(provider)

        assert serializer.data

    def test_deserialize(self):
        provider = baker.prepare(Provider, phone="+542494377777", email="test@email.com")
        provider_fields = [field.name for field in Provider._meta.get_fields()]
        valid_serialized_data = {
            k: v for (k, v) in provider.__dict__.items() if k in provider_fields and k != "id"
        } | {"phone": "+542494377777"}

        serializer = ProviderSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}


    @pytest.mark.parametrize("wrong_field", (
        {"phone": "a"},
        {"email": "breakingemail"},
        {"language": "breakinglanguage"},
        {"currency": "breakingcurrency"},
    ))
    def test_deserialize(self, wrong_field: dict):
        provider = baker.prepare(Provider, phone="+542494377777", email="test@email.com")
        provider_fields = [field.name for field in Provider._meta.get_fields()]
        valid_serialized_data = {
            k: v for (k, v) in provider.__dict__.items() if k in provider_fields and k != "id"
        } | {"phone": "+542494377777"} | wrong_field

        serializer = ProviderSerializer(data=valid_serialized_data)

        assert not serializer.is_valid()
        assert serializer.errors != {}