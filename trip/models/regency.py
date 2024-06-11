from django.db import models

class Regency(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey('trip.Province', on_delete=models.CASCADE, related_name='regencies')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'regencies'