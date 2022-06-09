from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.viewsets import ModelViewSet

from provider.api.serializers import ProviderSerializer, ServiceAreaSerializer
from provider.models import Provider, ServiceArea


class ProviderModelViewset(ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    @method_decorator(cache_page(60*60*2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class ServiceAreaModelViewset(ModelViewSet):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all().select_related("provider")

    @method_decorator(cache_page(60*60*2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)