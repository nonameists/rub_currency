import pytest
from unittest.mock import MagicMock, patch

from currency_api.services import CurrencyService


@pytest.mark.django_db
class TestCurrencyService:

    @pytest.fixture
    def currency_service(self):
        currencies = {'USD', 'EUR'}
        date = '2023-08-02'
        return CurrencyService(currencies, date)

    def test_get_rates_from_db(self, currency_service, mocker):
        mocker.patch.object(
            currency_service,
            '_get_data_from_db',
            return_value={'currencies': [{'name': 'USD', 'rate': 70.0}, {'name': 'EUR', 'rate': 80.0}]}
        )

        result = currency_service.get_rates()
        assert 'currencies' in result
        assert len(result['currencies']) == 2
        assert result['currencies'][0]['name'] == 'USD'
        assert result['currencies'][1]['name'] == 'EUR'

    def test_get_rates_from_archive(self, currency_service, mocker):
        mocker.patch.object(currency_service, '_is_date_archive', return_value=True)
        mocker.patch.object(
            currency_service,
            '_get_data_from_archive',
            return_value={'currencies': [{'name': 'USD', 'rate': 75.0}, {'name': 'EUR', 'rate': 85.0}]}
        )

        result = currency_service.get_rates()
        assert 'currencies' in result
        assert len(result['currencies']) == 2
        assert result['currencies'][0]['name'] == 'USD'
        assert result['currencies'][1]['name'] == 'EUR'

    def test_get_rates_from_future_date(self, currency_service, mocker):
        mocker.patch.object(currency_service, '_is_date_future', return_value=True)

        result = currency_service.get_rates()
        assert 'currencies' in result
        assert len(result['currencies']) == 0  # No rates for future dates

