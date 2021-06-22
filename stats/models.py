from django.db import models

from django_countries.fields import CountryField

# Create your models here.
class CountColor(models.Model):
    country = CountryField()
    color = models.CharField('Color', max_length=50)
