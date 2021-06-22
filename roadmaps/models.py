from django.db import models

from collections import defaultdict
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel

from django_countries.fields import CountryField

# Create your models here.
class RoadmapPage(Page):
    body = RichTextField(verbose_name='body', blank=True)
    country = CountryField()

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('country', classname="Country"),
        FieldPanel('body', classname="body"),
    ]

class RoadmapPageIndex(Page):
    body = RichTextField(verbose_name='body', blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]


    def get_context(self, request):
        context = super().get_context(request)
        rmaps = RoadmapPage.objects.all()
        rmap_dict = defaultdict(list)

        for obj in rmaps:
            rmap_dict[str(obj.country)].append(obj)
        context['rmaps'] = rmap_dict
        return context