# Generated by Django 3.0.8 on 2020-07-16 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0002_auto_20200716_1247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='collection',
        ),
    ]
