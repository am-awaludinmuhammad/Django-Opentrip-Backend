# Generated by Django 5.0.6 on 2024-06-24 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0007_alter_tripitinerary_activities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tripitinerary',
            name='activities',
        ),
        migrations.RemoveField(
            model_name='tripitinerary',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='tripitinerary',
            name='time_start',
        ),
        migrations.AddField(
            model_name='tripitinerary',
            name='activity',
            field=models.CharField(default=None),
        ),
        migrations.AddField(
            model_name='tripitinerary',
            name='time',
            field=models.TimeField(default=None),
        ),
    ]
