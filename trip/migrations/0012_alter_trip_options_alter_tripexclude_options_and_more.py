# Generated by Django 5.0.6 on 2024-07-10 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0011_trip_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='tripexclude',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='tripgallery',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='tripinclude',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='tripitinerary',
            options={'ordering': ['created_at']},
        ),
    ]
