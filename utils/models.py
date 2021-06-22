import shortuuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

def gen_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = shortuuid.uuid() + '.' + ext
    
    return 'home/%s' % (filename)

# Create your models here.
class Tag(models.Model):
    text = models.CharField('text', max_length=300)
    slug = models.SlugField(blank=True, null=True)
    parent = models.ForeignKey('self',  on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.text

class SiteData(models.Model):
    key = models.CharField('Key', max_length=50)
    val = models.TextField(blank=True, null=True)
    ftype = models.CharField('Ftype', max_length=50, default='text')
    val_file = models.ImageField(upload_to=gen_file_name, blank=True, null=True)
    val_arr = ArrayField(models.IntegerField(), default=list)