# Generated by Django 5.0.6 on 2024-06-19 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0005_rename_description_tripexclude_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tripitinerary',
            name='activity',
        ),
        migrations.AddField(
            model_name='tripitinerary',
            name='activities',
            field=models.JSONField(null=True),
        ),
        migrations.CreateModel(
            name='TripGallery',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='trip/galleries/')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_galleries', to='trip.trip')),
            ],
            options={
                'db_table': 'trip_galleries',
            },
        ),
    ]
