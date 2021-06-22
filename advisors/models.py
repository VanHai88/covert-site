import shortuuid

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from wagtail.snippets.models import register_snippet
# Create your models here.

def gen_file_name(instance, filename):
    return 'advisors/%s.png' % (shortuuid.uuid())

@register_snippet
class AdvisorProfile(models.Model):
    image = ProcessedImageField(
        upload_to=gen_file_name,
        processors=[ResizeToFill(200, 200)],
        format='PNG',
        options={'quality': 90}, blank=True, null=True
    )
    name = models.CharField('Name', max_length=300)
    description = models.TextField()
    order = models.IntegerField(default=0)


    def __str__(self):
        return self.name