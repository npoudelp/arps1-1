from django.db import models

# Create your models here.

class Fields(models.Model):
    name = models.CharField(max_length=35, default='Demo Field', blank=False)
    crop = models.CharField(max_length=35, default="None" ,null=True, blank=True)
    coordinates = models.TextField(null=False, blank=False)
    nitrogen = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)
    harvested = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.name
    

class FrequentQuestions(models.Model):
    question = models.TextField(null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    

class Plantation(models.Model):
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    crop = models.CharField(max_length=35, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.crop
    

class FertilizerAddition(models.Model):
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    name = models.CharField(max_length=35, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return self.name
    

class PestControl(models.Model):
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    name = models.CharField(max_length=35, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return self.name
    

class Irrigation(models.Model):
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=35, null=False, blank=False)
    
    def __str__(self):
        return self.field.name
    

class Harvest(models.Model):
    field = models.ForeignKey(Fields, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    crop = models.CharField(max_length=35, null=False, blank=False)
    quantity = models.FloatField(null=False, blank=False)
    
    def __str__(self):
        return self.field.name
    

class PinnedLocation(models.Model):
    location = models.CharField(max_length=35, null=False, blank=False)
    
    def __str__(self):
        return self.location