# Generated by Django 5.1.3 on 2024-11-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartbtech', '0007_reading_energy_consumption_reading_runtime_seconds_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='energy_consumption',
            field=models.FloatField(default=0.0),
        ),
    ]
