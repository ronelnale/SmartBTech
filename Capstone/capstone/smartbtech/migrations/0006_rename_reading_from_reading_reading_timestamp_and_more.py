# Generated by Django 5.0.6 on 2024-10-18 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartbtech', '0005_rename_energy_consumption_reading_pres_energy_rdg_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reading',
            old_name='reading_from',
            new_name='reading_timestamp',
        ),
        migrations.RemoveField(
            model_name='buildingincharge',
            name='reading',
        ),
        migrations.RemoveField(
            model_name='reading',
            name='kwh_used',
        ),
        migrations.RemoveField(
            model_name='reading',
            name='pres_energy_rdg',
        ),
        migrations.RemoveField(
            model_name='reading',
            name='prev_energy_rdg',
        ),
        migrations.RemoveField(
            model_name='reading',
            name='reading_to',
        ),
    ]
