from datetime import datetime
from typing import Set, Optional

import requests
from django.utils import timezone


class CurrencyService:
    CURRENCY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
    CURRENCY_ARCHIVE_URL = "https://www.cbr-xml-daily.ru/archive/{YEAR}/{MONTH}/{DAY}/daily_json.js"

    def __init__(self, currencies: Set[str], date: Optional[str]):
        self.currencies = currencies
        if date is None:
            self.date = str(timezone.now().date())
        else:
            self.date = date

    def get_rates(self):
        return self._get_data_from_source()

    def _get_data_from_source(self):
        result = {
            'date': self.date,
            "currencies": []
        }
        is_archive = self._is_date_archive(self.date)
        if is_archive:
            year, month, day = self.date.split('-')
            url = self.CURRENCY_ARCHIVE_URL.format(YEAR=year, MONTH=month, DAY=day)
        else:
            url = self.CURRENCY_URL

        request = requests.get(url)
        request.raise_for_status()
        raw_data = request.json()

        for currency in self.currencies:
            if currency in raw_data['Valute']:
                result['currencies'].append(
                    {'name': currency, 'rate': raw_data['Valute'][currency]['Value']}
                )
        return result

    def _is_date_archive(self, input_date: str) -> bool:
        try:
            input_date = datetime.strptime(input_date, '%Y-%m-%d').date()
            current_date = datetime.now().date()

            if input_date < current_date:
                return True
            return False
        except ValueError:
            return False
