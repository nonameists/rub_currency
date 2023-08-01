# Generated by Django 4.2.3 on 2023-07-31 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_from', to='currency_api.currency')),
                ('currency_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rates_to', to='currency_api.currency')),
            ],
        ),
    ]