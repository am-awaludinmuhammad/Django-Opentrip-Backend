from django.contrib import admin
from trip.models import Province, Regency, District

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Regency)
class RegencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'province')
    list_filter = ('province',)

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'regency')
    list_filter = ('regency',)
