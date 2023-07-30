from rest_framework import serializers


class DateSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=['%Y-%m-%d'], required=False)


class CurrencyRequestParamSerializer(DateSerializer):
    CURRENCY_CHOICES = [
        ('EUR', 'EUR'),
        ('USD', 'USD')
    ]

    currencies = serializers.MultipleChoiceField(choices=CURRENCY_CHOICES, required=True)


class CurrencyRateSerializer(serializers.Serializer):
    name = serializers.CharField()
    rate = serializers.FloatField()


class CurrenciesBaseSerializer(DateSerializer):
    currencies = CurrencyRateSerializer(many=True)




