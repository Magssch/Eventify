# Generated by Django 2.1.7 on 2019-03-12 12:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20190312_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='registration_starts',
            field=models.DateField(default=datetime.datetime(2019, 3, 12, 12, 3, 40, 70563, tzinfo=utc)),
        ),
    ]
