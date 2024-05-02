from django.db import models

# Create your models here.

class TR2(models.Model):
    Age = models.IntegerField()
    CD = models.DecimalField(max_digits=30, decimal_places=25)