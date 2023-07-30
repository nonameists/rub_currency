from typing import Dict

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from currency_api.serializers import CurrencyRequestParamSerializer, CurrenciesBaseSerializer
from currency_api.services import CurrencyService


class GetCurrency(GenericAPIView):

    def get(self, request: Request):
        ser: CurrencyRequestParamSerializer = CurrencyRequestParamSerializer(
            data=request.query_params, context=self.get_serializer_context()
        )
        ser.is_valid(raise_exception=True)
        rate_service: CurrencyService = CurrencyService(**ser.data)
        raw_result: Dict = rate_service.get_rates()
        result: CurrenciesBaseSerializer = CurrenciesBaseSerializer(raw_result)

        return Response(result.data, status=status.HTTP_200_OK)
