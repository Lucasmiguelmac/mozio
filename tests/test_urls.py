import pytest
from django.urls import resolve, reverse


class TestProviderURLs:
    @pytest.mark.parametrize('url_name, expected_path, kwargs, viewname',[
        ('provider-list',   '/api/providers/',      None,       'ProviderModelViewset'),
        ('provider-detail', '/api/providers/1/',    {'pk': 1},  'ProviderModelViewset'),
    ])
    def test_url_name(self, url_name, expected_path, kwargs, viewname):
        url = reverse(url_name, kwargs=kwargs)
        assert url == expected_path

        resolver = resolve(expected_path)
        assert resolver.func.__name__ == viewname

class TestServiceAreaURLs:
    @pytest.mark.parametrize('url_name, expected_path, kwargs, viewname',[
        ('servicearea-list',   '/api/service_areas/',      None,       'ServiceAreaModelViewset'),
        ('servicearea-detail', '/api/service_areas/1/',    {'pk': 1},  'ServiceAreaModelViewset'),
    ])
    def test_url_name(self, url_name, expected_path, kwargs, viewname):
        url = reverse(url_name, kwargs=kwargs)
        assert url == expected_path

        resolver = resolve(expected_path)
        assert resolver.func.__name__ == viewname