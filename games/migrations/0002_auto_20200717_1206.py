# Generated by Django 3.0.8 on 2020-07-17 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='collectionname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
