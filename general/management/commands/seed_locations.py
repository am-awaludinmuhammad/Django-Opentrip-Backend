import csv
import os
from django.core.management.base import BaseCommand
from trip.models import Province, Regency, District
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds the Province data from a CSV file'

    def handle(self, *args, **kwargs):
        provinces_csv = os.path.join(settings.BASE_DIR, 'provinces.csv')
        regencies_csv = os.path.join(settings.BASE_DIR, 'regencies.csv')
        districts_csv = os.path.join(settings.BASE_DIR, 'districts.csv')
        
        # seed provinces
        with open(provinces_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Province.objects.get_or_create(id=row['id'], name=row['name'])

        # seed regencies
        with open(regencies_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                province = Province.objects.get(pk=row['province_id'])
                Regency.objects.get_or_create(id=row['id'], name=row['name'], province=province)

        # seed districts
        with open(districts_csv, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                regency = Regency.objects.get(pk=row['regency_id'])
                District.objects.get_or_create(id=row['id'], name=row['name'], regency=regency)