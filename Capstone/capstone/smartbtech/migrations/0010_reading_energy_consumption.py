# Generated by Django 5.1.3 on 2024-11-21 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartbtech', '0009_remove_reading_energy_consumption_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='energy_consumption',
            field=models.FloatField(default=0.0),
        ),
    ]
