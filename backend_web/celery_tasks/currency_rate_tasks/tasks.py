import requests
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from backend.settings import CURRENCY_URL, CURRENCIES, MAIN_CURRENCY
from currency_api.models import Currency, ExchangeRate


@shared_task
@transaction.atomic
def currency_daily_rate_task() -> str:
    """Task fetch data from cbrf to get new currency rates for RUB-USD, RUB-EUR."""
    today_date = timezone.now().date()
    cbrf_data = []

    request = requests.get(CURRENCY_URL)
    request.raise_for_status()
    raw_data = request.json()

    for currency in CURRENCIES:
        if currency in raw_data["Valute"]:
            cbrf_data.append(
                {"name": currency, "rate": raw_data["Valute"][currency]["Value"]}
            )

    currencies_list = CURRENCIES + [MAIN_CURRENCY]

    currencies_from_db = Currency.objects.filter(name__in=currencies_list)
    currencies_map = {currency.name: currency.id for currency in currencies_from_db}

    new_rates = []

    for rate_item in cbrf_data:
        from_currency_rate = "RUB"
        to_currency_name = rate_item["name"]
        rate = rate_item["rate"]

        from_id = currencies_map[from_currency_rate]
        to_id = currencies_map[to_currency_name]

        new_rates.append(
            ExchangeRate(currency_from_id=from_id, currency_to_id=to_id, date=today_date, rate=rate)
        )

    total_items = ExchangeRate.objects.bulk_create(new_rates)

    return f"Task completed for {total_items} new rates."









