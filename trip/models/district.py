from django.db import models

class District(models.Model):
    name = models.CharField(max_length=100)
    regency = models.ForeignKey('trip.Regency', on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'districts'