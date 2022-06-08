from django.urls import include, path
from rest_framework import routers

from provider.api.views import ProviderModelViewset

router = routers.DefaultRouter()
router.register(r'providers', ProviderModelViewset)

urlpatterns = [
    path('', include(router.urls)),
]
