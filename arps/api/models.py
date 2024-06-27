from django.db import models

# Create your models here.

class Fields(models.Model):
    name = models.CharField(max_length=35, default='Demo Field', blank=False)
    coordinates = models.TextField(null=False, blank=False)
    nitrogen = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name