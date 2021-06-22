from django.db import models

# Create your models here.
class Route(models.Model):
    old = models.CharField('Old', max_length=300)
    new = models.CharField('New', max_length=300)