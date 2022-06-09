from rest_framework.viewsets import ModelViewSet

from provider.api.serializers import ProviderSerializer, ServiceAreaSerializer
from provider.models import Provider, ServiceArea


class ProviderModelViewset(ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

class ServiceAreaModelViewset(ModelViewSet):
    serializer_class = ServiceAreaSerializer
    queryset = ServiceArea.objects.all().select_related("provider")