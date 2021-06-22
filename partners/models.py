import shortuuid

from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet

def gen_file_name(instance, filename):
    return 'partners/%s.png' % (shortuuid.uuid())

PCHOICES = (
    ('fixed', 'fixed'),
    ('self-serve', 'self-serve')
)

@register_snippet
class Partner(models.Model):
    logo = ProcessedImageField(upload_to=gen_file_name,
                                           processors=[ResizeToFit(600, 600)],
                                           format='PNG',
                                           options={'quality': 90}, blank=True, null=True)
    name = models.CharField('Partner', max_length=50)
    description = models.TextField()
    row = models.IntegerField(default=0)
    ptype = models.CharField('Partner Type', choices=PCHOICES, max_length=50, default="fixed")
    
    panels = [
        FieldPanel('logo'),
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('ptype')
    ]


    def __str__(self):
        return self.name

    @property
    def get_logo(self):
        if self.logo:
            return self.logo.url
        else:
            return ''

@register_snippet
class EventPartner(models.Model):
    logo = ProcessedImageField(upload_to=gen_file_name,
                                           processors=[ResizeToFit(600, 600)],
                                           format='PNG',
                                           options={'quality': 90}, blank=True, null=True)
    name = models.CharField('Partner', max_length=50)
    
    panels = [
        FieldPanel('logo'),
        FieldPanel('name'),
    ]


    def __str__(self):
        return self.name

    @property
    def get_logo(self):
        if self.logo:
            return self.logo.url
        else:
            return ''