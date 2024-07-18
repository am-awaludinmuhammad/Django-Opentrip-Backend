from django.db import models

class TimeStampedModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Bank(TimeStampedModel):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=20)
    number = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)    

    class Meta:
        ordering = ['created_at']
        db_table = 'banks'