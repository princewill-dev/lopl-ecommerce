# Generated by Django 4.2.6 on 2023-11-21 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api_v1', '0003_alter_apikey_api_key_alter_passwordreset_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='api_key',
            field=models.CharField(default='p7Uvetm2fInRZn6CH1zmhzibOTyf5ySR', max_length=255),
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 21, 21, 7, 57, 606647, tzinfo=datetime.timezone.utc)),
        ),
    ]
