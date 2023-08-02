from datetime import datetime
from typing import Set, Optional, Dict

import requests
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.utils import timezone
from requests import HTTPError, Request

from backend.settings import CURRENCY_ARCHIVE_URL, MAIN_CURRENCY, CURRENCY_URL
from currency_api.exceptions import DateNotFoundException
from currency_api.models import ExchangeRate


class CurrencyService:

    def __init__(self, currencies: Set[str], date: Optional[str]):
        self.currencies = currencies
        if date is None:
            self.date = str(timezone.now().date())
        else:
            self.date = date

        self.result: Dict = {
            'date': self.date,
            "currencies": []
        }

    def get_rates(self) -> Dict:
        """Public method to get currency rates."""
        is_archive: bool = self._is_date_archive()
        if is_archive:
            return self._get_data_from_archive()
        is_future: bool = self._is_date_future()
        if is_future:
            return self.result

        return self._get_data_from_db()

    def _get_data_from_db(self) -> Dict:
        """Private method to fetch rates from db."""
        cached_rates = self._get_data_from_cache()
        if cached_rates:
            return cached_rates

        rates: QuerySet = ExchangeRate.objects.filter(
            currency_from__name=MAIN_CURRENCY, currency_to__name__in=self.currencies, date=self.date
        ).values('currency_to__name', 'rate')

        if not rates:
            self._get_data_from_source()
        for rate_item in rates:
            self.result['currencies'].append(
                {'name': rate_item['currency_to__name'], 'rate': rate_item['rate']}
            )
        self._put_data_to_cache(self.result)
        return self.result

    def _get_data_from_archive(self) -> Dict:
        """Private method call cbrf endpoint to get archived rates data."""
        year, month, day = self.date.split('-')
        url = CURRENCY_ARCHIVE_URL.format(YEAR=year, MONTH=month, DAY=day)
        request = requests.get(url)
        try:
            request.raise_for_status()
            raw_data = request.json()
        except HTTPError as error:
            if request.status_code == 404:
                raise DateNotFoundException()
            raise error
        return self._prepare_raw_data(raw_data)

    def _is_date_future(self) -> bool:
        """Private method check if date is future date."""
        try:
            input_date: datetime.date = datetime.strptime(self.date, '%Y-%m-%d').date()
            current_date: datetime.date = datetime.now().date()

            if input_date > current_date:
                return True
            return False
        except ValueError:
            return False

    def _is_date_archive(self) -> bool:
        """Private method check if input_date less than current_date."""
        try:
            input_date: datetime.date = datetime.strptime(self.date, '%Y-%m-%d').date()
            current_date: datetime.date = datetime.now().date()

            if input_date < current_date:
                return True
            return False
        except ValueError:
            return False

    def _prepare_raw_data(self, raw_data: Dict) -> Dict:
        """Private method prepare raw result from cbrf archive."""
        for currency in self.currencies:
            if currency in raw_data['Valute']:
                self.result['currencies'].append(
                    {'name': currency, 'rate': raw_data['Valute'][currency]['Value']}
                )
        return self.result

    def _get_data_from_source(self) -> Dict:
        """Private method fetch data from cbrf and execute delayed task to save data to db."""
        url: str = CURRENCY_URL
        request: Request = requests.get(url)

        request.raise_for_status()
        raw_data: Dict = request.json()

        return self._prepare_raw_data(raw_data)

    def _get_data_from_cache(self) -> Optional[Dict]:
        """Private method fetch data from Redis cache."""
        cached_data = cache.get(self.date)
        if cached_data:
            return cached_data
        return None

    def _put_data_to_cache(self, data: Dict) -> None:
        """Private method put data to Redis cache."""
        cache.set(self.date, data)
