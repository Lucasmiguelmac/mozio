from django.contrib.gis.geos import Point
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from provider.api.serializers import ProviderSerializer, ServiceAreaSerializer
from provider.models import Provider, ServiceArea


class ProviderModelViewset(ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ServiceAreaModelViewset(ModelViewSet):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all().select_related("provider")

    @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AvailableProvidersApiView(ListAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

    @method_decorator(cache_page(60 * 60 * 4))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        lat, lng = (
            float(self.request.GET["lat"]),
            float(self.request.GET["lng"])
        )
        point = Point(lat, lng)
        providers = Provider.objects.filter(
            service_area__area__contains=point
        )
        return providers