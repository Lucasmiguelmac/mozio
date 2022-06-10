from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('api/', include('provider.api.urls')),
    path('docs/', include_docs_urls(title='Providers & Service Areas API')),
]
