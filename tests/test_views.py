import json

import pytest
from django.urls import reverse
from django_mock_queries.mocks import MockSet
from model_bakery import baker
from rest_framework.serializers import ModelSerializer

from provider.api.serializers import ProviderSerializer, ServiceAreaSerializer
from provider.api.views import ProviderModelViewset, ServiceAreaModelViewset
from provider.models import Provider, ServiceArea

provider_fields = [
    field.name for field in Provider._meta.get_fields()
    if (not field.name in ProviderSerializer.Meta.exclude and field.name != "servicearea")
]


class TestProviderViewset:

    prepare_provider = (lambda self=None: baker.prepare(
        Provider, phone="+542494377777", email="test@email.com"
    ))
    provider_1 = prepare_provider()
    valid_data_dict = {
        k: v for (k, v) in provider_1.__dict__.items() if k in provider_fields
    } | {"phone": str(provider_1.phone)}

    def test_list(self, mocker, rf):
        # Arrange
        qs = MockSet(
            self.provider_1,
            self.prepare_provider(),
            self.prepare_provider(),
        )
        url = reverse('provider-list')
        request = rf.get(url)
        view = ProviderModelViewset.as_view(
            {'get': 'list'}
        )
        # Mcking
        mocker.patch.object(
            ProviderModelViewset, 'get_queryset', return_value=qs
        )
        # Act
        response = view(request).render()
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf):
        url = reverse('provider-detail', kwargs={'pk': self.provider_1.id})
        request = rf.get(url)
        mocker.patch.object(
            ProviderModelViewset, 'get_queryset', return_value=MockSet(self.provider_1)
        )
        view = ProviderModelViewset.as_view(
            {'get': 'retrieve'}
        )

        response = view(request, pk=self.provider_1.id).render()

        assert response.status_code == 200

    def test_create(self, mocker, rf):
        url = reverse('provider-list')
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(self.valid_data_dict)
        )
        save_mock = mocker.patch.object(
            ProviderSerializer, 'save'
        )
        view = ProviderModelViewset.as_view(
            {'post': 'create'}
        )

        response = view(request).render()

        assert response.status_code == 201
        save_mock.assert_called()

    def test_update(self, mocker, rf):
        url = reverse('provider-detail', kwargs={'pk': self.provider_1.id})
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(self.valid_data_dict)
        )
        mocker.patch.object(
            ProviderModelViewset, 'get_object', return_value=self.provider_1
        )
        save_mock = mocker.patch.object(
            ProviderSerializer, 'save'
        )
        view = ProviderModelViewset.as_view(
            {'put': 'update'}
        )

        response = view(request, pk=self.provider_1.id).render()

        assert response.status_code == 200
        save_mock.assert_called()

    @pytest.mark.parametrize('field', provider_fields)
    def test_partial_update(self, mocker, rf, field):
        field_value = self.provider_1.__dict__[field]
        valid_field = str(field_value) if field == "phone" else field_value
        url = reverse('provider-detail', kwargs={'pk': self.provider_1.id})
        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps({field: valid_field})
        )
        mocker.patch.object(
            ProviderModelViewset, 'get_object', return_value=self.provider_1
        )
        save_mock = mocker.patch.object(
            Provider, 'save'
        )
        view = ProviderModelViewset.as_view(
            {'patch': 'partial_update'}
        )

        response = view(request).render()

        assert response.status_code == 200
        save_mock.assert_called()

    def test_delete(self, mocker, rf):
        url = reverse('provider-detail', kwargs={'pk': self.provider_1.id})
        request = rf.delete(url)
        mocker.patch.object(
            ProviderModelViewset, 'get_object', return_value=self.provider_1
        )
        del_mock = mocker.patch.object(
            Provider, 'delete'
        )
        view = ProviderModelViewset.as_view(
            {'delete': 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        del_mock.assert_called()


service_area_fields = [
    field.name for field in ServiceArea._meta.get_fields()
]


class TestServiceAreaModelViewset:

    prepare_service_area = (lambda self=None: baker.prepare(
        ServiceArea, provider_id=1,
    ))
    service_area_1 = baker.prepare(ServiceArea, provider_id=1)
    valid_serialized_data = {
        k: v for (k, v) in service_area_1.__dict__.items() if k in service_area_fields and k != "id"
    } | {"price": float(service_area_1.price)} | {"provider": service_area_1.provider_id}

    def test_list(self, mocker, rf):
        # Arrange
        qs = MockSet(
            self.service_area_1,
            self.prepare_service_area(),
            self.prepare_service_area(),
        )
        url = reverse('servicearea-list')
        request = rf.get(url)
        view = ServiceAreaModelViewset.as_view(
            {'get': 'list'}
        )
        # Mocking
        mocker.patch.object(
            ServiceAreaModelViewset, 'get_queryset', return_value=qs
        )
        # Act
        response = view(request).render()
        # Assert
        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf):
        url = reverse('servicearea-detail',
                      kwargs={'pk': self.service_area_1.id})
        request = rf.get(url)
        mocker.patch.object(
            ServiceAreaModelViewset, 'get_queryset', return_value=MockSet(self.service_area_1)
        )
        view = ServiceAreaModelViewset.as_view(
            {'get': 'retrieve'}
        )

        response = view(request, pk=self.service_area_1.id).render()

        assert response.status_code == 200

    def test_create(self, mocker, rf):
        provider = baker.prepare(
            Provider, phone="+542494377777", email="test@email.com", id=1,
        )
        service_area = baker.prepare(
            ServiceArea, provider=provider,
        )
        url = reverse('servicearea-list')
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(self.valid_serialized_data)
        )
        to_internal_value_mock = mocker.patch(
            'rest_framework.relations.PrimaryKeyRelatedField.to_internal_value',
            return_value=service_area
        )
        save_mock = mocker.patch.object(
            ServiceAreaSerializer, 'save'
        )
        view = ServiceAreaModelViewset.as_view(
            {'post': 'create'}
        )

        response = view(request).render()

        assert response.status_code == 201
        to_internal_value_mock.assert_called()
        save_mock.assert_called()

    def test_update(self, mocker, rf):
        url = reverse('servicearea-detail', kwargs={'pk': self.service_area_1.id})
        request = rf.put(
            url,
            content_type='application/json',
            data=json.dumps(self.valid_serialized_data)
        )
        mocker.patch.object(
            ServiceAreaModelViewset, 'get_object', return_value=self.service_area_1
        )
        to_internal_value_mock = mocker.patch(
            'rest_framework.relations.PrimaryKeyRelatedField.to_internal_value',
            return_value=self.service_area_1,
        )
        save_mock = mocker.patch.object(
            ServiceAreaSerializer, 'save'
        )
        view = ServiceAreaModelViewset.as_view(
            {'put': 'update'}
        )

        response = view(request, pk=self.service_area_1.id).render()

        assert response.status_code == 200
        to_internal_value_mock.assert_called()
        save_mock.assert_called()

    @pytest.mark.parametrize(
        'field',
        valid_serialized_data.keys()
    )
    def test_partial_update(self, mocker, rf, field):
        provider = baker.prepare(
            Provider, phone="+542494377777", email="test@email.com", id=1,
        )
        service_area = baker.prepare(
            ServiceArea, provider=provider, id=1
        )
        field_value = self.valid_serialized_data[field]
        url = reverse('servicearea-detail', kwargs={'pk': service_area.id})
        request = rf.patch(
            url,
            content_type='application/json',
            data=json.dumps({field: field_value})
        )
        mocker.patch.object(
            ServiceAreaModelViewset, 'get_object', return_value=service_area
        )
        mocker.patch(
            'rest_framework.validators.qs_exists', return_value=True
        )
        mocker.patch.object(
            ServiceAreaSerializer,
            'get_unique_together_validators',
            return_value=[],
        )
        mocker.patch(
            'rest_framework.relations.PrimaryKeyRelatedField.to_internal_value',
            return_value=provider,
        )
        save_mock = mocker.patch.object(
            ServiceArea, 'save'
        )
        view = ServiceAreaModelViewset.as_view(
            {'patch': 'partial_update'}
        )

        response = view(request).render()

        assert response.status_code == 200
        save_mock.assert_called()

    def test_delete(self, mocker, rf):
        url = reverse('servicearea-detail', kwargs={'pk': self.service_area_1.id})
        request = rf.delete(url)
        mocker.patch.object(
            ServiceAreaModelViewset, 'get_object', return_value=self.service_area_1
        )
        del_mock = mocker.patch.object(
            ServiceArea, 'delete'
        )
        view = ServiceAreaModelViewset.as_view(
            {'delete': 'destroy'}
        )

        response = view(request).render()

        assert response.status_code == 204
        del_mock.assert_called()