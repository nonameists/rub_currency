from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class ExchangeRate(models.Model):
    currency_from = models.ForeignKey(Currency, related_name='rates_from', on_delete=models.CASCADE)
    currency_to = models.ForeignKey(Currency, related_name='rates_to', on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.currency_from} to {self.currency_to} - {self.rate} on {self.date}"
