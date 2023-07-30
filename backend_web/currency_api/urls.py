from django.urls import path

from .views import GetCurrency

urlpatterns = [
    path("currency", GetCurrency.as_view(), name="get_currency_rate"),
]