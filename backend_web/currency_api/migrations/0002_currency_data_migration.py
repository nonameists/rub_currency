from django.db import migrations


def create_initial_currencies(apps, schema_editor):
    currency_model = apps.get_model('currency_api', 'Currency')

    currencies = ['RUB', 'USD', 'EUR']

    new_currencies = [currency_model(name=c_name) for c_name in currencies]
    currency_model.objects.bulk_create(new_currencies)


class Migration(migrations.Migration):

    dependencies = [
        ('currency_api', '0001_add_currency_and_rate_tables'),
    ]

    operations = [
        migrations.RunPython(create_initial_currencies)
    ]
