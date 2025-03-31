# Generated by Django 5.1.3 on 2024-11-21 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smartbtech', '0006_rename_reading_from_reading_reading_timestamp_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='energy_consumption',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reading',
            name='runtime_seconds',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reading',
            name='watt_seconds',
            field=models.FloatField(default=0.0),
        ),
    ]
