# Generated by Django 2.1.5 on 2019-03-12 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20190227_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='has_paid',
            field=models.BooleanField(default=False),
        ),
    ]
