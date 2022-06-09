import pytest
from django.urls import resolve, reverse


class TestEndpointsURLs:
    @pytest.mark.parametrize('url_name, expected_path, kwargs, viewname',[
        ('provider-list',   '/api/providers/',      None,       'ProviderModelViewset'),
        ('provider-detail', '/api/providers/1/',    {'pk': 1},  'ProviderModelViewset'),
    ])
    def test_url_name(self, url_name, expected_path, kwargs, viewname):
        url = reverse(url_name, kwargs=kwargs)
        assert url == expected_path

        resolver = resolve(expected_path)
        assert resolver.func.__name__ == viewname
