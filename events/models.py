import requests
import shortuuid

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils import timezone

from datetime import date
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFit, ResizeToFill

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core import blocks
from wagtail.core.blocks import CharBlock, ListBlock, RichTextBlock, StructBlock
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel, MultiFieldPanel
from wagtailgeowidget.edit_handlers import GeoPanel
from wagtailgeowidget.helpers import geosgeometry_str_to_struct
from wagtail.snippets.edit_handlers import SnippetChooserPanel

BM_SETTINGS = settings.BIG_MARKER_SETTINGS

def gen_file_name(instance, filename):
    return 'events/%s.png' % (shortuuid.uuid())


class EventPartner(Orderable, models.Model):
    event = ParentalKey('events.Event', on_delete=models.CASCADE, related_name='event_partner')
    partner = models.ForeignKey('partners.EventPartner', on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('partner'),
    ]

    def __str__(self):
        return self.event.title + " -> " + self.partner.name

ECHOICES = (
        ('physical', 'Physical'),
        ('webinar', 'Webinar'),
    )

class Event(Page):
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    etype = models.CharField('Event Type', choices=ECHOICES, default='physical', max_length=50)
    bm_id = models.CharField('BM ID', blank=True, null=True, max_length=50)
    banner = ProcessedImageField(upload_to=gen_file_name,
                                           processors=[ResizeToFill(1920, 1260)],
                                           format='JPEG',
                                           options={'quality': 80}, blank=True, null=True)
    
    banner_thumb = ImageSpecField(source='banner',
                                      processors=[ResizeToFill(300, 197)],
                                      format='JPEG',
                                      options={'quality': 65})

    reg_url = models.URLField(blank=True, null=True)
    body = RichTextField(verbose_name='body', blank=True)

    content_panels = Page.content_panels + [
        InlinePanel('event_partner', label='Partners'),
        FieldPanel('start'),
        FieldPanel('end'),
        FieldPanel('etype'),
        FieldPanel('reg_url'),
        MultiFieldPanel([
            FieldPanel('address'),
            GeoPanel('location', address_field='address'),
        ], 'Geo details'),
        FieldPanel('banner'),
        FieldPanel('body', classname="full"),
    ]

    @property
    def eactive(self):
        return self.start > timezone.now()

    @property
    def get_banner(self):
        if self.banner:
            return self.banner.url
        else:
            return ''

    @property
    def get_banner_thumb(self):
        if self.banner:
            return self.banner_thumb.url
        else:
            return ''

    def get_context(self, request):
        context = super(Event, self).get_context(request)
        context['partners'] = self.event_partner.all().prefetch_related('partner')
        return context

    @cached_property
    def point(self):
        return geosgeometry_str_to_struct(self.location)

    @property
    def lat(self):
        return self.point['y']

    @property
    def lng(self):
        return self.point['x']

    @property
    def pdate(self):
        tstring = '%s - %s' % (self.start.strftime('%-I:%M %p') , self.end.strftime('%-I:%M %p'))
        return [self.start.year, self.start.day, self.start.strftime('%b'), tstring]

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.etype == 'webinar':
                headers = {'API-KEY': BM_SETTINGS['key']}
                payload = {"channel_id": BM_SETTINGS['channel'], 
                           "title": self.title,
                           "start_time": self.start.strftime('%Y-%m-%d %H:%M')}
                r = requests.post(BM_SETTINGS['url'] + 'conferences/', headers=headers, data=payload)
                self.bm_id = r.json()['id']

            
        return super().save(*args, **kwargs)


class EventPageIndex(Page):
    # ...
    def events(self):
        # Get list of live event pages that are descendants of this page
        events = Event.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        events = events.filter(date_from__gte=date.today())

        # Order by date
        events = events.order_by('title')

        return events

    def get_context(self, request):
        context = super().get_context(request)

        context['years'] = range(2019, date.today().year + 1)
        
        return context