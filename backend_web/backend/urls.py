from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("currency_api.urls")),
    path("admin/", admin.site.urls),
]