# Generated by Django 4.2.6 on 2023-11-21 20:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api_v1', '0002_alter_apikey_api_key_alter_passwordreset_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='api_key',
            field=models.CharField(default='oaS1aMhC0finyHHyYAMRCb1WuIepqr0J', max_length=255),
        ),
        migrations.AlterField(
            model_name='passwordreset',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 21, 21, 6, 45, 114359, tzinfo=datetime.timezone.utc)),
        ),
    ]