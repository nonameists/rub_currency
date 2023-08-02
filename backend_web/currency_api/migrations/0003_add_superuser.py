import os

from django.db import migrations
from django.contrib.auth.models import User


def create_superuser(apps, schema_editor):
    superuser = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpassword'
    )

    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ('currency_api', '0002_currency_data_migration'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
