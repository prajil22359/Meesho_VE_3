from django.db import models

# Create your models here.

class Prediction(models.Model):
    image = models.ImageField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=100)
    pattern = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    sleeve = models.CharField(max_length=100)
    neckline = models.CharField(max_length=100)
    fit = models.CharField(max_length=100)
    occasion = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    confidence = models.FloatField()
