from rest_framework.viewsets import ModelViewSet

from provider.api.serializers import ProviderSerializer
from provider.models import Provider


class ProviderModelViewset(ModelViewSet):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()