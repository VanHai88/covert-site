import shortuuid

from collections import OrderedDict
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel

def gen_file_name(instance, filename):

    extension = filename.split('.')[-1].lower()

    return 'media-releases/%s.%s' % (shortuuid.uuid(), extension)

# Create your models here.
class Release(Page):
    pdf = models.FileField(upload_to=gen_file_name)
    date = models.DateField()

    content_panels = Page.content_panels + [
        FieldPanel('pdf'),
        FieldPanel('date'),
    ]

class ReleasePageIndex(Page):
    # ...
    def releases(self):
        # Get list of live event pages that are descendants of this page
        releases = []

        return releases 


    def get_context(self, request):
        context = super().get_context(request)
        
        rel_dict = OrderedDict()
        rels = Release.objects.all().order_by('-date')
        
        for item in rels:
            rel_dict.setdefault(item.date.year, [])
            rel_dict[item.date.year].append(item)

        context['releases'] = rel_dict
        
        return context