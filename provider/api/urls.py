from django.urls import include, path
from rest_framework import routers

from provider.api.views import (AvailableProvidersApiView,
                                ProviderModelViewset, ServiceAreaModelViewset)

router = routers.DefaultRouter()
router.register(r'providers', ProviderModelViewset)
router.register(r'service_areas', ServiceAreaModelViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('available-providers/', AvailableProvidersApiView.as_view(), name="available-providers")
]
