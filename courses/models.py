import shortuuid

from django import forms
from django.db import models
from django.contrib.postgres.fields import ArrayField

from collections import defaultdict
from datetime import date, timedelta
from djmoney.models.fields import MoneyField
from django_countries.fields import CountryField
from django_select2.forms import Select2MultipleWidget
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.core.blocks import (
    CharBlock,
    ListBlock,
    RichTextBlock,
    TextBlock,
    StructBlock,
    StreamBlock
)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    StreamFieldPanel
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from utils.fields import GroupedModelChoiceField

from utils.models import Tag


def gen_file_name(instance, filename):
    return 'courses/%s.png' % (shortuuid.uuid())

class ModelFieldPanel(FieldPanel):
    def on_form_bound(self):
        self.form.fields['ctags'].queryset = Tag.objects.all()
        super().on_form_bound()

class TestimonialBlock(StructBlock):
    name = CharBlock(label="Name")
    text = TextBlock(label="Text")
    title = CharBlock(label="Title", required=False)

    class Meta:
        icon = 'placeholder'
        label = 'Testimonial'
        template = "courses/testimonial.html"

class DetailsBlock(StructBlock):
    overview = RichTextBlock()
    details = RichTextBlock()
    included = ListBlock(CharBlock(label="Item"))
    fees = RichTextBlock()
    registration = RichTextBlock()
    ideal_for = ListBlock(CharBlock(label="Item"))
    contact = CharBlock()
    email = CharBlock()

    testimonials = StreamBlock([
        ('testimonials', TestimonialBlock())
    ], required=False)

    class Meta:
        icon = 'placeholder'
        label = 'Course Details'
        template = "courses/details.html"

@register_snippet
class Session(models.Model):
    dates = ArrayField(models.DateField())

    panels = [
        FieldPanel('dates'),
    ]

    def __str__(self):
        return '|'.join([str(x) for x in self.dates])


class CourseSession(Orderable, models.Model):
    course = ParentalKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='course_session'
    )
    session = models.ForeignKey(
        'courses.Session', on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('session'),
    ]

    def __str__(self):
        return self.course.title + " -> " + self.session.__str__()


class CoursePartner(Orderable, models.Model):
    course = ParentalKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='course_partner'
    )
    partner = models.ForeignKey(
        'partners.Partner', on_delete=models.CASCADE, related_name='+')

    panels = [
        SnippetChooserPanel('partner'),
    ]

    def __str__(self):
        return self.course.title + " -> " + self.partner.name


class Course(Page):
    banner = ProcessedImageField(
        upload_to=gen_file_name,
        processors=[ResizeToFill(750, 500)],
        format='PNG',
        options={'quality': 90}, blank=True, null=True
    )

    banner_thumb = ImageSpecField(source='banner',
                                    processors=[ResizeToFill(300, 197)],
                                    format='JPEG',
                                    options={'quality': 65})

    badge = ProcessedImageField(
        upload_to=gen_file_name,
        processors=[ResizeToFit(250, 250)],
        format='PNG',
        options={'quality': 90}, blank=True, null=True
    )

    body = StreamField([
        ('details', DetailsBlock())
    ])

    
    signup = models.URLField()
    price = MoneyField(max_digits=14, decimal_places=2)
    description = models.TextField()
    ctags = ParentalManyToManyField(Tag)
    promoted = models.BooleanField(default=False)
    countries = CountryField(multiple=True)

    content_panels = Page.content_panels + [
        InlinePanel('course_session', label='Sessions'),
        InlinePanel('course_partner', label='Partners'),
        FieldPanel('signup'),
        FieldPanel('description'),
        FieldPanel('price'),
        FieldPanel('promoted'),
        FieldPanel('banner'),
        FieldPanel('countries', widget=Select2MultipleWidget),
        ModelFieldPanel('ctags', widget=forms.CheckboxSelectMultiple),
        FieldPanel('badge'),
        StreamFieldPanel('body'),
    ]

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
            
    @property
    def get_badge(self):
        if self.badge:
            return self.badge.url
        else:
            return ''

    def get_context(self, request):
        context = super(Course, self).get_context(request)
        context['partners'] = self.course_partner.all().prefetch_related('partner')

        ctype = 'fixed'
        for obj in context['partners']:
            if obj.partner.ptype != 'fixed':
                ctype = 'self-serve'
        context['ctype'] = ctype

        context['sessions'] = sorted([x.session.dates for x in self.course_session.all().prefetch_related(
            'session') if x.session.dates[0] > (date.today() + timedelta(days=1))], key=lambda x: x[0])

        return context


class CoursePageIndex(Page):
    # ...
    def courses(self):
        # Get list of live event pages that are descendants of this page
        #courses = Course.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        #events = events.filter(date_from__gte=date.today())

        # Order by date
        #events = events.order_by('title')

        return []

    def get_context(self, request):
        context = super().get_context(request)
        
        tags = Tag.objects.exclude(parent=None).prefetch_related('parent').order_by('id')

        tags_dict = defaultdict(list)
        for obj in tags:
            tags_dict[obj.parent.text].append(obj)    

        context['tags_dict'] = tags_dict
        
        return context

    